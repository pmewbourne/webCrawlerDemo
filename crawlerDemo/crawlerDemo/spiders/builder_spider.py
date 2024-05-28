# In order to run this, navigate to webCrawlerDemo/crawlerDemo via the command line, then execute "scrapy crawl buildCrawler"

# CrawlSpider is for the crawler, Rule is for the behavior, linkExtractor is for accessing the domains.
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
# CloseSpider is for quitting out of the spider
from scrapy.exceptions import CloseSpider


class crawlingSpiderDemo(CrawlSpider):
    # fields:
    # crawlCounter - tracks how many items have been logged, used to track when to quit
    # name - How crawler is referred to in terminal
    # allowed_domains - controls the scope of the urls that the crawler will attempt to access
    # start_urls - where the crawler will start searching from
    crawlCounter = 0

    name = "buildCrawler"
    allowed_domains = ["thebuilderssupply.com"]
    start_urls = ["https://thebuilderssupply.com/"]

    # Control behavior of spider, differing from default
    custom_settings = {"FEED_URI": "theBuilderSupply_%(time)s.csv", # Output results to this file name
                       "FEED_FORMAT": "csv", # File type of output
                       "DUPEFILTER_CLASS": 'scrapy.dupefilters.RFPDupeFilter', # Supposed to stop crawler from revisiting same url multiple times
                       "DUPEFILTER_DEBUG":True, # Also supposed to stop crawler from revisiting same url multiple times
                       }


    rules = (
        Rule(LinkExtractor(deny = ["/checkout.asp","/add_cart.asp", "/view_cart.asp", "/error.asp", # These were determined by the robots.txt from the website
                           "/shipquote.asp", "/rssfeed.asp", "/mobile/", "/cgi-bin/",
                           "/private/", "/admin/", "/checkout/", "/cart/", "/account/"]
                           ), follow = True, callback = "parse_item"), # Follow to get more than just what's on the hoempage
    )
    
    def parse_item(self, response):
        """
        input: response, the current page being scraped
        output: returns a dictionary containing the name of an item, its number, its price, and its stock amount.
        """
        # Get the info first to check if it's empty
        item_name = response.css(".product-details h2::text").extract_first()
        item_num = response.css(".product-id span[itemprop='sku']::text").extract_first()
        price = response.css("span[id='price']::text").extract_first()
        stock = response.css("span[id='availability']::text").extract_first()
        if item_name: # A non-item page will return a null item name. Check we are logging an item and not attempting to log null.
            self.crawlCounter += 1 # increment total number of items logged
            if self.crawlCounter > 150: # Quit if it's a certain amount. The website has thousands of items and 
                                        # there's a bug where domains get revisited. Don't want to be stuck running forever.
                raise CloseSpider(reason = "Max Items Reached")
            yield {
                "item name": item_name,
                "item number": item_num.replace(":","").strip(),
                "price": price.replace("$",""),
                "stock": stock.replace(" In stock","")
                }
        else: # If not an item page, just move on.
            yield