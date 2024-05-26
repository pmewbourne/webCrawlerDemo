# Adapted from https://www.youtube.com/watch?v=m_3gjHGxIJc

# This sets up a webCrawler that crawls books.toscrape.com, a website made for rudimentary webscraping. 
# This crawler crawls books.toscrape.com and iterates through all of the books on the website. 
# It takes the title, price, and stock number of each and stores each value in a dictionary

# Imports:
# This crawler is made using scrapy. 
# CrawlSpider is for the crawler, Rule is for the behavior, linkExtractor is for accessing the domains.
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


# Params:
# name - How we can refer to the crawler in terminal
# allowed_domains - controls the scope of the urls that the crawler will attempt to access
# start_urls - where the crawler will start searching from
class crawlingSpiderDemo(CrawlSpider):

    name = "crawler1"
    allowed_domains = ["toscrape.com"] 
    start_urls = ["http://books.toscrape.com/"]
    # The format of books.toscrape.com is simple. Besides the home page, all pages fall under catalogue pages. 
    # If it's a category page, it is a list of books in a sepcific genre. If it's not a category page,
    # it's the listing of a book.

    # PROXY_SERVER = "127.0.0.1" 
    # Here, we could put in a proxy server if needed. This would circumvent our ip being blocked from repeated requests by using multiple different ips.

    # Two rules for the crawler:
    # 1. Iterate through all the categories
    # 2. Iterate through all the books and make their info a dictionary
    rules = (
        Rule(LinkExtractor(allow = "catalogue/category")),
        Rule(LinkExtractor(allow = "catalogue", deny = "category"), callback = "parse_item")
    )

    # Function to parse the current page and get the info of a book
    def parse_item(self, response):
        """
        input: response, the current page being scraped
        output: returns a dictionary containing the title, price, and stock number of a book.
        """
        # Have to use css style to access these page elements
        yield {
            "title": response.css(".product_main h1::text").get(),
            "price": response.css(".price_color::text").get(),
            # This next one's messy because of how messy the page is. I think I could clean it up.
            "availability": response.css(".availability::text")[1].get().replace("\n", "").replace(" ", "").replace("Instock", "").replace("available", "").replace("(", "").replace(")","")
        }