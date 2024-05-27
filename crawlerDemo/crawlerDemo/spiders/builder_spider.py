from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class crawlingSpiderDemo(CrawlSpider):

    name = "buildCrawler"
    allowed_domains = ["thebuilderssupply.com"]
    start_urls = ["https://thebuilderssupply.com/"]

    custom_settings = {"FEED_URI": "theBuilderSupply_%(time)s.csv", 
                       "FEED_FORMAT": "csv",
                       "DUPEFILTER_CLASS": 'scrapy.dupefilters.RFPDupeFilter',
                       }

    rules = (
        Rule(LinkExtractor(deny = ["/checkout.asp","/add_cart.asp", "/view_cart.asp", "/error.asp",
                           "/shipquote.asp", "/rssfeed.asp", "/mobile/", "/cgi-bin/",
                           "/private/", "/admin/", "/checkout/", "/cart/", "/account/"]
                           ), follow = True, callback = "parse_item"),
    )
    
    def parse_item(self, response):
        item_name = response.css(".product-details h2::text").extract()
        item_num = response.css(".product-id span[itemprop='sku']::text").extract_first()
        price = response.css("span[id='price']::text").extract_first()
        stock = response.css("span[id='availability']::text").extract_first()
        if item_name:
            yield {
                "item name": item_name ,
                "item number": item_num.replace(":","").strip(),
                "price": price.replace("$",""),
                "stock": stock.replace(" In stock","")
                }
        else:
            yield