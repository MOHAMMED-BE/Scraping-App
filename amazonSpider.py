# from crypt import methods
# from itertools import product
import json
# from flask import request, session
import scrapy
# from datetime import date
# from productTracker.items import ProductesItem
# from scrapy.loader import ItemLoader
# import requests
# from forms import ScrapingForm

# from App import product
# from classes.Functions import getProduct
# from App import app,mysql

from jumiaSpider import query

# from classes.Function import getProduct



class amazon(scrapy.Spider ):
    name = 'amazon'

    # def getProduct():
    #     with app.app_context():
    #         cursor = mysql.connection.cursor()
    #         cursor.execute('SELECT name from product order by date desc LIMIT 1')
    #         # product = get_results(cursor)

    #         product = cursor.fetchall()
    #         # res = product
    #         # res = str(res)
        
    #         query = str(product)

    #     char_to_replace = {
    #             ',': '',
    #             '(' : '',
    #             ')' : '',
    #             '\'': ''}

    #     def getQuery(text):
    #         for key, value in char_to_replace.items():
    #             text = text.replace(key, value)
    #         return str(text)

    #     query = getQuery(query)
    #     return query

    query = query
    # query = "iPhone 13 pro max"

    # form = ScrapingForm()
    # if request.method == "POST":
    #     if form.validate_on_submit():
    #         product_name = request.form["product_name"]


    
    def __init__(self, query=query, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # if "product_name" in session:
        #     query = session['product_name']

        # pro = requests.sessions()

        # query = pro['product_name']

        self.base_url = "https://www.amazon.com"
        self.search_url = "https://www.amazon.com/s?k={query}"

        self.rank = None
        self.page_num = 1
        self.query = query

        self.start_urls = [self.search_url.format(
            query=query.replace(" ", "+")
        )]

    def parse(self, response):


        
        # search_results = response.css("div.s-result-item "
        #                               "h2 > a > span::text").getall()
        yield scrapy.Request(str(self.start_urls))


        # if title in search_results:
        #     page_pos = ( search_results.index(title) + 1 )
        #     self.rank = (self.page_num - 1) * 48 + page_pos

        # else:
            # not found
        data = {}
        
        self.page_num += 1

        products = response.css("div.s-result-item")

        title = products.css("div.s-card-container > div.a-section div.a-section > div.a-section > h2 > a > span.a-text-normal::text").getall()
        price = products.css("div.a-section span.a-price span.a-price-whole::text").getall()
        # title = title.replace(',','')
        data[self.query] = {
            'title':title,
            'price':price
        }

        listObj = {}
        content = {
                "key": [
                    "value"
                ]
            }

        with open("amazonDataScraping.json","w") as file:
            json.dump(content, file)

        listObj.update(data)

        with open("amazonDataScraping.json", 'w') as json_file:
            json.dump(listObj, json_file)








        # for product in products:

            # loader = ItemLoader(item=ProductesItem(),selector=product)
            # loader.add_css('title',"div.s-card-container > div.a-section div.a-section > div.a-section > h2 > a > span.a-text-normal::text")
            # # loader.add_css('title',".a-text-normal::text")
            # loader.add_css('price',"div.a-section span.a-price span.a-price-whole::text")
            # # loader.add_css('price',"div.a-section > div > div > div > div.a-section > div.a-row span.a-price span.a-price-whole::text")
            
            # yield loader.load_item()
            
        
        # next_btn = response.css("a.s-pagination-next")


        # if next_btn and self.page_num < 7:
        #     next_page = f"{self.start_urls[0]}/{next_btn.attrib['href']}"
        #     yield scrapy.Request(url=next_page)












































            
            # else:
            #     self.rank = "Not found!"
        
    #     self.export()

    # def export(self):
    #     today = date.today().strftime("%d-%m-%Y")

    #     with open("track.json") as file:
    #         data = json.load(file)

    #     if self.query in data:
    #         data = {
    #             today: self.rank
    #         }
    #     else:
    #         data   = {
    #             today: self.rank
    #         }

    #     with open("track.json", "w") as file:
    #         # data = data.decode("utf-8")
    #         json.dump(data, file)