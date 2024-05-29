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
    name = "chessCrawler"
    # allowed_domains = ["chesspathways.com"]
    # start_urls = ["https://chesspathways.com"]
    rule_domains = ""

    custom_settings = {"ROBOTSTXT_OBEY":True}

    def __init__(self, filename = None, *args, **kwargs):
        super(crawlingSpiderDemo, self).__init__(*args, **kwargs)
        if filename:
            with open(filename, 'r') as f:
                fileArgs = f.readlines()
                self.start_urls = [fileArgs[0].strip()]
                self.allowed_domains = [fileArgs[1].strip()]
                self.rule_domains = [fileArgs[2].strip()]
                crawlingSpiderDemo.rules = (
                    Rule(LinkExtractor(allow = self.rule_domains), callback = "parse_item", follow = True),
                )

                

    # rules = (
    #     Rule(LinkExtractor(allow = rule_domains), callback = "parse_item"),
    # )
    
    # Function to parse the current page and get the info of a chess opening
    def parse_item(self, response):
        """
        input: response, the current page being scraped
        output: returns a dictionary containing the name of a chess opening and what broad section it falls under.
        """
        yield {
            # Have to use css style to access these page elements
            "title":response.css(".hgroup h1::text").get(),
            "section":response.css('ol.breadcrumbs li:nth-child(3) span[itemprop="name"]::text').get()
        }