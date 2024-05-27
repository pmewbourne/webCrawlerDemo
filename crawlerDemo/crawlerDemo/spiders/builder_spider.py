from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class crawlingSpiderDemo(CrawlSpider):

    name = "buildCrawler"
    allowed_domains = ["thebuildersupply.com"]
    start_urls = ["https://thebuilderssupply.com/"]

    custom_settings = {"FEED_URI": "theBuilderSupply_%(time)s.csv", 
                       "FEED_FORMAT": "csv"}

    rules = (
        Rule(LinkExtractor(deny = ["/checkout.asp","/add_cart.asp", "/view_cart.asp", "/error.asp",
                           "/shipquote.asp", "/rssfeed.asp", "/mobile/", "/cgi-bin/",
                           "/private/", "/admin/", "/checkout/", "/cart/", "/account/"]
                           ), callback = "parse_item"),
    )
    
    def parse_item(self, response):
        yield {
            "item name":response.css(".product-details h2::text").extract(),
            "item number": response.css(".product-id span[itemprop='sku']::text").extract_first().replace(":","").strip(),
            "price":response.css("span[id='price']::text").extract_first().replace("$",""),
            "stock":response.css("span[id='availability']::text").extract_first().replace(" In stock","")
            }