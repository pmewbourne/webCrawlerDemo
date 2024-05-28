# Adapted from https://www.youtube.com/watch?v=m_3gjHGxIJc

# In order to run this, navigate to webCrawlerDemo/crawlerDemo via the command line, then execute "scrapy crawl crawler1"

# This sets up a webCrawler that crawls books.toscrape.com, a website made for rudimentary webscraping. 
# This crawler crawls books.toscrape.com and iterates through all of the books on the website. 
# It takes the title, price, and stock number of each and stores each value in a dictionary


# CrawlSpider is for the crawler, Rule is for the behavior, linkExtractor is for accessing the domains.
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor



class crawlingSpiderDemo(CrawlSpider):
    # fields:
    # name - How crawler is referred to in terminal
    # allowed_domains - controls the scope of the urls that the crawler will attempt to access
    # start_urls - where the crawler will start searching from

    name = "crawler1"
    allowed_domains = ["toscrape.com"] 
    start_urls = ["http://books.toscrape.com/"]

    # Format of books.toscrape.com: all pages fall under catalogue pages. 
    # If it's a category page, it is a list of books. Else, it's just a book

    # PROXY_SERVER = "127.0.0.1" 
    # Putting in proxy server prevents ip blockage from repeated requests.

    rules = (
        Rule(LinkExtractor(allow = "catalogue/category")), # Iterate through categories
        Rule(LinkExtractor(allow = "catalogue", deny = "category"), callback = "parse_item") #Iterate through all books and make into dict
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
            "availability": response.css(".availability::text")[1].get().replace("In stock (", "").replace("available)", "").strip()
        }