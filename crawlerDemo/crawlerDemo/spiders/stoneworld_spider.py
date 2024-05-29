# Only slightly changed from before. Wanted practice doing it on a new website. 
# Other comments are copied from crawling_spider.py

# In order to run this, navigate to webCrawlerDemo/crawlerDemo via the command line, then execute "scrapy crawl chessCrawler"

# CrawlSpider is for the crawler, Rule is for the behavior, linkExtractor is for accessing the domains.
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class crawlingSpiderDemo(CrawlSpider):

    # fields:
    # name - How crawler is referred to in terminal
    # allowed_domains - controls the scope of the urls that the crawler will attempt to access
    # start_urls - where the crawler will start searching from
    name = "stoneworldCrawler"
    crawl_domains = ""
    info_domains = ""

    css_companyName = ""
    css_companyAddress = ""
    css_companyCity = ""
    css_companyCountry = ""
    css_companyPhone = ""
    css_companyFax = ""
    css_companyURL = ""
    css_companyEmail = ""
    css_contactName = ""
    css_contactPhone = ""
    css_contactEmail = ""

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
                self.css_companyName = fileArgs[4].strip()
                self.css_companyAddress = fileArgs[5].strip()
                self.css_companyCity = fileArgs[6].strip()
                self.css_companyCountry = fileArgs[7].strip()
                self.css_companyPhone = fileArgs[8].strip()
                self.css_companyFax = fileArgs[9].strip()
                self.css_companyURL = fileArgs[10].strip()
                self.css_companyEmail = fileArgs[11].strip()
                self.css_contactName = fileArgs[12].strip()
                self.css_contactPhone = fileArgs[13].strip()
                self.css_contactEmail = fileArgs[14].strip()
                # Adapted from https://stackoverflow.com/questions/27509489/how-to-dynamically-set-scrapy-rules
                crawlingSpiderDemo.rules = (Rule (LinkExtractor(allow=(self.crawl_domains)),  follow= True),
                                            Rule (LinkExtractor(allow=(self.info_domains)), callback="parse_item",  follow= True))
                super(crawlingSpiderDemo, self)._compile_rules()

                

    # rules = (
    #     Rule(LinkExtractor(allow = rule_domains), callback = "parse_item"),
    # )
    
    # Function to parse the current page and get the info of a chess opening
    def parse_item(self, response):
        """
        input: response, the current page being scraped
        output: returns a dictionary containing the name of a chess opening and what broad section it falls under.
        """
        companyName = response.css(self.css_companyName)
        companyAddress = response.css(self.css_companyAddress)
        companyCity = response.css(self.css_companyCity)
        companyCountry = response.css(self.css_companyCountry)
        companyPhone = response.css(self.css_companyPhone)
        companyFax = response.css(self.css_companyFax)
        companyURL = response.css(self.css_companyURL)
        companyEmail = response.css(self.css_companyEmail)
        contactName = response.css(self.css_contactName)
        contactPhone = response.css(self.css_contactPhone)
        contactEmail = response.css(self.css_contactEmail)
        yield {
            
            # Have to use css style to access these page elements
            "title":response.css(self.css1).get(),
            "section":response.css(self.css2).get()
        }