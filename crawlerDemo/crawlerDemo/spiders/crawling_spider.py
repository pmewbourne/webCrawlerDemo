# Adapted from https://www.youtube.com/watch?v=m_3gjHGxIJc

# This sets up a webCrawler that crawls books.toscrape.com, a website made for rudimentary webscraping. 
# This crawler crawls books.toscrape.com and iterates through all of the books on the website. 
# It takes the title, price, and stock number of each, stores each value in a dictionary, and outputs that dictionary to a json file.

# Imports:
# This crawler is made using scrapy. We need CrawlSpider for the crawler itself, Rule for defining the crawler's behavior, 
# and LinkExtractor to control where it goes.
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

# Defining the crawler:
# We create a class that is based off the "CrawlSpider" class from scrapy.
# Params:
# name - How we can refer to the crawler in terminal
# allowed_domains - controls the scope of the urls that the crawler will attempt to access
# start_urls - where the crawler will start searching from
class crawlingSpiderDemo(CrawlSpider):

    name = "crawler1"
    allowed_domains = ["toscrape.com"] # We only want this crawler to look through the books.toscrape.com website, so we limit it to toscrape.com domains.
    start_urls = ["http://books.toscrape.com/"] # And we start it off on the homepage of that website
    # The format of books.toscrape.com is simple. Besides the home page, all pages fall under catalogue pages. 
    # If it's a category page, it is a list of books in that genre. If it's not a category page,
    # it's the page of a book.

    # PROXY_SERVER = "127.0.0.1" # Here, we could put in a proxy server if needed. This would circumvent our ip being blocked from repeated requests by using multiple different ips.

    # Next, we define the rules of how the crawler will operate. As a first step, it'll just iterate though all of the categories on the website, visiting each one.
    # As a second step, it'll iterate though all of the books on the website. For each one, we call a function that creates a dictionary pertaining to that book.
    # Depending on the command line run of the crawler, you can output a list of these disctionaries. (For example, here I used scrapy crawl crawler1 -0 output.json)
    rules = (
        Rule(LinkExtractor(allow = "catalogue/category")),
        Rule(LinkExtractor(allow = "catalogue", deny = "category"), callback = "parse_item")
    )

    # Function parse_item:
    # Params - 
    def parse_item(self, response):
        yield {
            "title": response.css(".product_main h1::text").get(),
            "price": response.css(".price_color::text").get(),
            "availability": response.css(".availability::text")[1].get().replace("\n", "").replace(" ", "").replace("Instock", "").replace("available", "").replace("(", "").replace(")","")
        }