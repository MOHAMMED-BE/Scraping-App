import json
import scrapy
from classes.Functions import getProductName

ProductName = getProductName()

class jumia(scrapy.Spider):
    name = 'jumia'
    
    def __init__(self, query=ProductName, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.base_url = "https://www.jumia.ma"
        self.search_url = "https://www.jumia.ma/catalog/?q={query}&sort=rating#catalog-listing"

        self.query = query

        self.start_urls = [self.search_url.format(
            query=query.replace(" ", "+")
        )]

    def parse(self, response):

        yield scrapy.Request(str(self.start_urls))

        data = {}
        
        products = response.css("div.-paxs")

        name = products.css("article.prd > a.core > div.info > h3.name::text").get()
        price = products.css("article.prd > a.core > div.info > div.prc::text").get()
        image = products.css("article.prd > a.core > div.img-c > img::attr(data-src)").get()
        
        data = {
        'name':name,
        'price':price,
        'image':image
        }

        with open("jumiaDataScraping.json", 'w') as file:
            json.dump(data, file)
