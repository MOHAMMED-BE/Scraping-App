from itertools import product
import json
from requests import request
import scrapy
from datetime import date
from scrapy.loader import ItemLoader
from os import path
from flask import request
from scrapy.crawler import CrawlerProcess
# from .webapp.app import varx
# from __future__ import unicode_literals
# from App import insert 
 
# from .webapp.app import varx



# from webapp import app

class jumia(scrapy.Spider):
    name = 'jumia'
    # varx = 'redmi note 11 S'

    
    def __init__(self, query="iPhone 13 pro max", *args, **kwargs):
        super().__init__(*args, **kwargs)

        # query = jumia.varx
        # query = app.scrape.varx

        self.base_url = "https://www.jumia.ma"
        self.search_url = "https://www.jumia.ma/catalog/?q={query}"

        self.rank = None
        self.page_num = 1
        self.query = query

        self.start_urls = [self.search_url.format(
            query=query.replace(" ", "+")
        )]

    def parse(self, response):

        yield scrapy.Request(str(self.start_urls))
        
        self.page_num += 1

        data = {}
        
        products = response.css("div.-paxs")

        title = products.css("article.prd > a.core > div.info > h3.name::text").getall()
        price = products.css("article.prd > a.core > div.info > div.prc::text").getall()
        oldPrice = products.css("article.prd > a.core > div.info > div.s-prc-w div.old::text").getall()
        
        data[self.query] = {
            'title':title,
            'price':price,
            'oldPrice':oldPrice
        }
        # yield data

        # prix = {}

        # filename = 'jumiaprice.json'
        # filename = 'D:\STAGE-LP\Flask-Scraping-App\Flask_Scraping_App\Flask_Scraping_App\spiders\jumiaprice.json'
        listObj = {}
        content = {
                "key": [
                    "value"
                ]
            }
        # listObj['item'] = inputvalue

        with open("jumiaDataScraping.json","w") as file:
            json.dump(content, file)

        listObj.update(data)
        # listObj.update(data)

        with open("jumiaDataScraping.json", 'w') as json_file:
            json.dump(listObj, json_file)


# # def run():
# process = CrawlerProcess()
# process.crawl(jumia)
# process.start() 
    # run scraper
  
# run()


































# class jumia(scrapy.Spider):
#     name = 'jumia'
#     varx = 'redmi note 11 pro 5G'
#     # cols = ["Title","Price","oldPrice"]
#     # start_urls = ["https://www.jumia.ma"]
#     # start_urls = ["https://www.jumia.ma/catalog/?q=iphone+13+pro+max"]
#     # start_urls = ["https://www.jumia.ma/catalog/?q=iPhone+13+pro+max&page=5#catalog-listing"]

    
#     def __init__(self, query="iPhone 13 pro max", *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         query = jumia.varx

#         self.base_url = "https://www.jumia.ma"
#         self.search_url = "https://www.jumia.ma/catalog/?q={query}"

#         self.rank = None
#         self.page_num = 1
#         self.query = query

#         self.start_urls = [self.search_url.format(
#             query=query.replace(" ", "+")
#         )]

#     def parse(self, response):

#         # l = request.form['']
        
#         # search_results = response.css("div.s-result-item "
#         #                               "h2 > a > span::text").getall()


#         # if title in search_results:
#         #     page_pos = ( search_results.index(title) + 1 )
#         #     self.rank = (self.page_num - 1) * 48 + page_pos

#         # else:
#             # not found

#         yield scrapy.Request(str(self.start_urls))
        
        
#         self.page_num += 1

#         data = {}
        
#         products = response.css("div.-paxs")
#         # for product in products:
#         #     # loader = ItemLoader(item=jumiaItem())
#         #     loader = ItemLoader(item=jumiaItem(),selector=product)
#         #     loader.add_css('title',"article.prd > a.core > div.info > h3.name::text")
#         #     loader.add_css('price',"article.prd > a.core > div.info > div.prc::text")
#         #     loader.add_css('oldPrice',"article.prd > a.core > div.info > div.s-prc-w div.old::text")
            
#         #     # loader.add_value('title',product.css("article.prd > a.core > div.info > h3.name::text").getall())
#         #     # loader.add_value('price',product.css("article.prd > a.core > div.info > div.prc::text").getall())
#         #     # loader.add_value('oldPrice',product.css("article.prd > a.core > div.info > div.s-prc-w div.old::text").getall())

#         #     yield loader.load_item()

#         title = products.css("article.prd > a.core > div.info > h3.name::text").getall()
#         price = products.css("article.prd > a.core > div.info > div.prc::text").getall()
#         oldPrice = products.css("article.prd > a.core > div.info > div.s-prc-w div.old::text").getall()
        
#         data[self.query] = {
#             'title':title,
#             'price':price,
#             'oldPrice':oldPrice
#         }
#         # yield data

#         # prix = {}

#         # filename = 'jumiaprice.json'
#         # filename = 'D:\STAGE-LP\Flask-Scraping-App\Flask_Scraping_App\Flask_Scraping_App\spiders\jumiaprice.json'
#         listObj = {}
#         content = {
#                 "key": [
#                     "value"
#                 ]
#             }
#         # listObj['item'] = inputvalue

#         with open("dataScraping.json","w") as file:
#             json.dump(content, file)

#         listObj.update(data)
#         # listObj.update(data)

#         with open("dataScraping.json", 'w') as json_file:
#             json.dump(listObj, json_file)

#         # for i in data['iphone 13 pro max']:
#         #     print(i['title'])

#         # with open("tracke.json","w") as file:
#         #     file.writelines()

#         # main driver

#         def run():
#             process = CrawlerProcess()
#             process.crawl(jumia)
#             process.start()

            
# # if __name__ == '__main__':
# #     # run scraper
# #     process = CrawlerProcess()
# #     process.crawl(jumia)
# #     process.start()   

#             # price = response.css("div.-paxs article.prd > a.core > div.info > h3.name::text")
            
        
#         # next_btn = response.css("div.pg-w a:nth-child(7)")


#         # if next_btn:
#         #     next_page = f"{self.start_urls[0]}&page={self.page_num}#catalog-listing"
#         #     yield scrapy.Request(url=next_page)






















            
#             # else:
#             #     self.rank = "Not found!"
        
#     #     self.export()

#     # def export(self):
#     #     today = date.today().strftime("%d-%m-%Y")

#     #     with open("track.json") as file:
#     #         data = json.load(file)

#     #     if self.query in data:
#     #         data = {
#     #             today: self.rank
#     #         }
#     #     else:
#     #         data   = {
#     #             today: self.rank
#     #         }

#     #     with open("track.json", "w") as file:
#     #         # data = data.decode("utf-8")
#     #         json.dump(data, file)