import json
import scrapy

class jumia(scrapy.Spider):
    name = 'usdtomad'
    start_urls = ["https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=MAD"]
   
    def parse(self, response):

        data = {}
        usd = response.css("p.result__BigRate-sc-1bsijpp-1::text").get()

        data[jumia.name] = {
            'usd':float(usd)
        }
        with open("usdtomad.json", 'w') as json_file:
            json.dump(data, json_file)

