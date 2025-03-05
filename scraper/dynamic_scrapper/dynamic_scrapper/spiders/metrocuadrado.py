import scrapy


class MetrocuadradoSpider(scrapy.Spider):
    name = "metrocuadrado"
    allowed_domains = ["test.com"]
    start_urls = ["https://test.com"]

    def parse(self, response):
        pass
