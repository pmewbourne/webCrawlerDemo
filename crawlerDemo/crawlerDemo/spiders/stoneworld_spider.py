
# In order to run this, navigate to webCrawlerDemo/crawlerDemo via the command line, then execute "scrapy crawl stoneworldCrawler -a filename=stoneworldCrawl.txt"
# -a sets a variable in the execute to be taken from the commandline
# filename= is setting that variable 
# stoneworldCrawl.txt is full of info for the crawler.

# CrawlSpider is for the crawler, Rule is for the behavior, linkExtractor is for accessing the domains.
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

# Used to clean up strings
import re


class crawlingSpiderDemo(CrawlSpider):

    # fields:
    # name - How crawler is referred to in terminal
    
    # crawl_domains will be set to domains to crawl
    # info_domains will be set to domains to scrape
    # cssDictList is a list of strings used for populating the csv
    # cssDictListLen will be set to the len of said list
    name = "stoneworldCrawler"
    crawl_domains = ""
    info_domains = ""
    cssDictList = []
    cssDictListLen = 0


    custom_settings = {"ROBOTSTXT_OBEY":True, # Follow the robots.txt of the website
                       "FEED_URI": "stoneWorld_%(time)s.csv", # Output results to this file name
                       "FEED_FORMAT": "csv", # File type of output
                       "DUPEFILTER_CLASS": 'scrapy.dupefilters.RFPDupeFilter', # Supposed to stop crawler from revisiting same url multiple times
                       "DUPEFILTER_DEBUG":True, # Also supposed to stop crawler from revisiting same url multiple times
                       }

    # Adapted from https://stackoverflow.com/questions/27865334/iterate-scrapy-crawl-over-several-text-files-containing-urls
    def __init__(self, filename = None, *args, **kwargs):
        super(crawlingSpiderDemo, self).__init__(*args, **kwargs)
        if filename:
            with open(filename, 'r') as f:
                # Take in the info from the .txt file and use it to set up the spider
                fileArgs = f.readlines()
                self.start_urls = [fileArgs[0].strip()]
                self.allowed_domains = [fileArgs[1].strip()]
                self.crawl_domains = [fileArgs[2].strip()]
                self.info_domains = [fileArgs[3].strip()]
                self.cssDictList = fileArgs[4:]
                self.cssDictListLen = len(self.cssDictList)
                # Adapted from https://stackoverflow.com/questions/27509489/how-to-dynamically-set-scrapy-rules
                crawlingSpiderDemo.rules = ( # Dynamic ules need to be set by editing the initializer b/c they're formed at compile time
                                            Rule (LinkExtractor(allow=(self.info_domains)), callback="parse_item",  follow= True),
                                            Rule (LinkExtractor(allow=(self.crawl_domains)),  follow= True),
                                            )
                super(crawlingSpiderDemo, self)._compile_rules()

                

    
    # Function to clean up the strings from webpages
    def stringCleaner(self, strToFix):
        """
        input: a string obtained through the css of a webpage
        output: a string without extraneous elements, like newline characters or redundant prefixes
        """
        if strToFix: # Chance the page lacks a specific element, maybe like fax number. Check first.
            cleanStr = strToFix.replace("\n","").replace("mailto:","").replace("Fax: ","").replace("Phone: ","").replace('"','').strip()
            # Adapted from https://www.codecademy.com/resources/docs/python/regex/sub
            cleanStr = re.sub(r'\s+',' ', cleanStr)
            return cleanStr
        else:
            return "Not Provided"

    # Function to parse the current page and get the info set by the input file
    def parse_item(self, response):
        """
        input: response, the current page being scraped
        output: returns a dictionary containing the name of a chess opening and what broad section it falls under.
        """
        returnDict = {}
        for i in range (0, self.cssDictListLen//2):
            # In input file, each elem of dictionary is a pair of lines, the key followed by value.
            curIndex = 2*i
            key = self.cssDictList[curIndex].strip()
            value = self.stringCleaner(response.css(self.cssDictList[curIndex + 1]).get())
            returnDict[key] = value
        yield returnDict
