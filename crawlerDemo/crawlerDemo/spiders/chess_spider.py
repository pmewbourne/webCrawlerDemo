from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class crawlingSpiderDemo(CrawlSpider):

    name = "chessCrawler"
    allowed_domains = ["chesspathways.com"]
    start_urls = ["https://chesspathways.com"]

    rules = (
        Rule(LinkExtractor(allow = "chess-openings"), callback = "parse_item"),
    )
    
    def parse_item(self, response):
        yield {
            "title":response.css(".hgroup h1::text").get(),
            "section":response.css('ol.breadcrumbs li:nth-child(3) span[itemprop="name"]::text').get()
        }