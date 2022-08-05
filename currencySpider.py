import json
import scrapy

class currencySpider(scrapy.Spider):
    name = 'currency'
    start_urls = ["https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=MAD"]
   
    def parse(self, response):

        data = {}
        currency = response.css("p.result__BigRate-sc-1bsijpp-1::text").get()

        data[currencySpider.name] = {
            'currency':float(currency)
        }
        with open("currencyScrapingData.json", 'w') as json_file:
            json.dump(data, json_file)

