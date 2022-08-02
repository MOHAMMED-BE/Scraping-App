# from crypt import methods
# import imp
# from itertools import product
import json
from flask import session
# from flask_mysqldb import MySQL
# from requests import request
# import requests
import scrapy
# from datetime import datetime
# from scrapy.loader import ItemLoader
# from os import path
# from flask import appcontext_popped, appcontext_pushed, appcontext_tearing_down, request, session
# from scrapy.crawler import CrawlerProcess
# from classes.dotDict import dotdict
# from  flask_session import Session
# from App import scrape
# from App import get_results,mysql
# mysql = MySQL(app)

# from flask_wtf import FlaskForm
# from forms import ScrapingForm

# from .webapp.app import varx
# from __future__ import unicode_literals
# from App import insert 
 
# from .webapp.app import varx

# from App import product

# from App import app,mysql
# from app import app
from classes.Functions import getJumiaProducts

query = getJumiaProducts()


class jumia(scrapy.Spider):
    name = 'jumia'
    # varx = 'redmi note 11 S'



    

    # # with app.app_context():
    # product_name= session["product_name"]

    

    
   
    
    
    def __init__(self, query=query, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # with app.app_context():
        #     form = ScrapingForm()
        #     if request.method == "POST":
        #         if form.validate_on_submit():
        #             product_name = request.form["product_name"]

        # pro = requests.sessions()

        # query = pro['product_name']


        # with appcontext_tearing_down.test_request_context():
        # if "product_name" in session:
        #     query = session['product_name']
        # query = product

        # query = app.scrape.varx

        
            # product = cursor.fetchall()
        
        # for i in product:
        #     product_name = i.name
        #     if i >1:
        #         break
        #     # query = product_name
    # productName = str(product)
        


        self.base_url = "https://www.jumia.ma"
        self.search_url = "https://www.jumia.ma/catalog/?q={query}"

        self.rank = None
        self.page_num = 1
        self.query = query

        self.start_urls = [self.search_url.format(
            query=query.replace(" ", "+")
        )]

    def parse(self, response):

        # with app.app_context():
        #     cursor = mysql.connection.cursor()
        #     cursor.execute('SELECT name from product LIMIT 1')
        #     # product = get_results(cursor)

        #     product = cursor.fetchall()

        #     res = product

        #     re = str(res)

            # for i in product

        yield scrapy.Request(str(self.start_urls))
        

        data = {}
        
        products = response.css("div.-paxs")

        name = products.css("article.prd > a.core > div.info > h3.name::text").getall()
        price = products.css("article.prd > a.core > div.info > div.prc::text").getall()
        oldPrice = products.css("article.prd > a.core > div.info > div.s-prc-w div.old::text").getall()
        image = products.css("article.prd > a.core > div.img-c > img::attr(data-src)").get()
        
        data[self.query] = {
        'name':name,
        'price':price,
        'oldPrice':oldPrice,
        'image':image
        }


        # yield data

        # price = {}

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
#     # cols = ["name","Price","oldPrice"]
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


#         # if name in search_results:
#         #     page_pos = ( search_results.index(name) + 1 )
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
#         #     loader.add_css('name',"article.prd > a.core > div.info > h3.name::text")
#         #     loader.add_css('price',"article.prd > a.core > div.info > div.prc::text")
#         #     loader.add_css('oldPrice',"article.prd > a.core > div.info > div.s-prc-w div.old::text")
            
#         #     # loader.add_value('name',product.css("article.prd > a.core > div.info > h3.name::text").getall())
#         #     # loader.add_value('price',product.css("article.prd > a.core > div.info > div.prc::text").getall())
#         #     # loader.add_value('oldPrice',product.css("article.prd > a.core > div.info > div.s-prc-w div.old::text").getall())

#         #     yield loader.load_item()

#         name = products.css("article.prd > a.core > div.info > h3.name::text").getall()
#         price = products.css("article.prd > a.core > div.info > div.prc::text").getall()
#         oldPrice = products.css("article.prd > a.core > div.info > div.s-prc-w div.old::text").getall()
        
#         data[self.query] = {
#             'name':name,
#             'price':price,
#             'oldPrice':oldPrice
#         }
#         # yield data

#         # price = {}

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
#         #     print(i['name'])

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