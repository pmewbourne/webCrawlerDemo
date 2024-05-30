# Only slightly changed from before. Wanted practice doing it on a new website. 
# Other comments are copied from crawling_spider.py

# In order to run this, navigate to webCrawlerDemo/crawlerDemo via the command line, then execute "scrapy crawl chessCrawler"

# CrawlSpider is for the crawler, Rule is for the behavior, linkExtractor is for accessing the domains.
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

import re


class crawlingSpiderDemo(CrawlSpider):

    # fields:
    # name - How crawler is referred to in terminal
    # allowed_domains - controls the scope of the urls that the crawler will attempt to access
    # start_urls - where the crawler will start searching from
    name = "stoneworldCrawler"
    crawl_domains = ""
    info_domains = ""
    cssDictList = []
    cssDictListLen = 0


    custom_settings = {"ROBOTSTXT_OBEY":True,
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
                fileArgs = f.readlines()
                self.start_urls = [fileArgs[0].strip()]
                self.allowed_domains = [fileArgs[1].strip()]
                self.crawl_domains = [fileArgs[2].strip()]
                self.info_domains = [fileArgs[3].strip()]
                cssFirstSlice = int(fileArgs[4])
                cssLastSlice = int(fileArgs[5])
                self.cssDictList = fileArgs[cssFirstSlice:cssLastSlice]
                self.cssDictListLen = len(self.cssDictList)
                # Adapted from https://stackoverflow.com/questions/27509489/how-to-dynamically-set-scrapy-rules
                crawlingSpiderDemo.rules = (
                                            Rule (LinkExtractor(allow=(self.info_domains)), callback="parse_item",  follow= True),
                                            Rule (LinkExtractor(allow=(self.crawl_domains)),  follow= True),
                                            )
                super(crawlingSpiderDemo, self)._compile_rules()

                

    
    
    def stringCleaner(self, strToFix):
        if strToFix:
            cleanStr = strToFix.replace("\n","").replace("mailto:","").replace("Fax: ","").replace("Phone: ","").replace('"','').strip()
            cleanStr = re.sub(r'\s+',' ', cleanStr)
            return cleanStr
        else:
            return "Not Provided"

    # Function to parse the current page and get the info of a chess opening
    def parse_item(self, response):
        """
        input: response, the current page being scraped
        output: returns a dictionary containing the name of a chess opening and what broad section it falls under.
        """
        returnDict = {}
        for i in range (0, self.cssDictListLen//2):
            curIndex = 2*i
            key = self.cssDictList[curIndex].strip()
            value = self.stringCleaner(response.css(self.cssDictList[curIndex + 1]).get())
            returnDict[key] = value
        yield returnDict
