import json
import scrapy
from jumiaSpider import ProductName


class amazon(scrapy.Spider ):
    name = 'amazon'
    
    def __init__(self, query=ProductName, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.base_url = "https://www.amazon.com"
        self.search_url = "https://www.amazon.com/s?k={query}"

        self.query = query

        self.start_urls = [self.search_url.format(
            query=query.replace(" ", "+")
        )]

    def parse(self, response):
        
        yield scrapy.Request(str(self.start_urls))

        data = {}
        
        products = response.css("div.s-result-item")

        name = products.css("div.s-card-container > div.a-section div.a-section > div.a-section > h2 > a > span.a-text-normal::text").get()
        price = products.css("div.a-section span.a-price span.a-price-whole::text").get()
        
        data = {
            'name':name,
            'price':float(price.replace(',',''))
        }

        with open("amazonDataScraping.json", 'w') as file:
            json.dump(data, file)
