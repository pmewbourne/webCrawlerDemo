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

    # css_companyName = ""
    # css_companyAddress = ""
    # css_companyCity = ""
    # css_companyCountry = ""
    # css_companyPhone = ""
    # css_companyFax = ""
    # css_companyURL = ""
    # css_companyEmail = ""
    # css_contactName = ""
    # css_contactPhone = ""
    # css_contactEmail = ""

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
                # self.css_companyName = fileArgs[4].strip()
                # self.css_companyAddress = fileArgs[5].strip()
                # self.css_companyCity = fileArgs[6].strip()
                # self.css_companyCountry = fileArgs[7].strip()
                # self.css_companyPhone = fileArgs[8].strip()
                # self.css_companyFax = fileArgs[9].strip()
                # self.css_companyURL = fileArgs[10].strip()
                # self.css_companyEmail = fileArgs[11].strip()
                # self.css_contactName = fileArgs[12].strip()
                # self.css_contactPhone = fileArgs[13].strip()
                # self.css_contactEmail = fileArgs[14].strip()
                # Adapted from https://stackoverflow.com/questions/27509489/how-to-dynamically-set-scrapy-rules
                crawlingSpiderDemo.rules = (
                                            Rule (LinkExtractor(allow=(self.info_domains)), callback="parse_item",  follow= True),
                                            Rule (LinkExtractor(allow=(self.crawl_domains)),  follow= True),
                                            )
                super(crawlingSpiderDemo, self)._compile_rules()

                

    # rules = (
    #     Rule(LinkExtractor(allow = rule_domains), callback = "parse_item"),
    # )
    
    
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
        # companyName = response.css(self.css_companyName).get()
        # companyAddress = response.css(self.css_companyAddress).get()
        # companyCity = response.css(self.css_companyCity).get()
        # companyCountry = response.css(self.css_companyCountry).get()
        # companyPhone = response.css(self.css_companyPhone).get()
        # companyFax = response.css(self.css_companyFax).get()
        # companyURL = response.css(self.css_companyURL).get()
        # companyEmail = response.css(self.css_companyEmail).get()
        # contactName = response.css(self.css_contactName).get()
        # contactPhone = response.css(self.css_contactPhone).get()
        # contactEmail = response.css(self.css_contactEmail).get()
        returnDict = {}
        for i in range (0, self.cssDictListLen//2):
            curIndex = 2*i
            key = self.cssDictList[curIndex].strip()
            value = self.stringCleaner(response.css(self.cssDictList[curIndex + 1]).get())
            returnDict[key] = value
        yield returnDict
        # yield {
            
            # Have to use css style to access these page elements
            # "Name":companyName.strip() if companyName else "Not Provided",
            # "Address":companyAddress.strip() if companyAddress else "Not Provided",
            # "City":companyCity.strip() if companyCity else "Not Provided",
            # "Country":companyCountry.strip() if companyCountry else "Not Provided",
            # "Phone Number":companyPhone.strip() if companyPhone else "Not Provided",
            # "Fax Number":companyFax.strip() if companyFax else "Not Provided",
            # "URL":companyURL.strip() if companyURL else "Not Provided",
            # "Email":companyEmail.replace("mailto:","").strip() if companyEmail else "Not Provided",
            # "Contact Name":contactName.strip() if contactName else "Not Provided",
            # "Contact Phone Number":contactPhone.strip() if contactPhone else "Not Provided",
            # "Contact Email":contactEmail.replace("mailto:","").strip() if contactEmail else "Not Provided"
        # }