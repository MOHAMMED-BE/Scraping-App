import json
import scrapy
from jumiaSpider import query


class amazon(scrapy.Spider ):
    name = 'amazon'
    query = query
    
    
    def __init__(self, query=query, *args, **kwargs):
        super().__init__(*args, **kwargs)

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


        # if name in search_results:
        #     page_pos = ( search_results.index(name) + 1 )
        #     self.rank = (self.page_num - 1) * 48 + page_pos

        # else:
            # not found
        data = {}
        
        self.page_num += 1

        products = response.css("div.s-result-item")

        name = products.css("div.s-card-container > div.a-section div.a-section > div.a-section > h2 > a > span.a-text-normal::text").getall()
        price = products.css("div.a-section span.a-price span.a-price-whole::text").getall()
        # name = name.replace(',','')


        
        data[self.query] = {
            'name':name,
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
            # loader.add_css('name',"div.s-card-container > div.a-section div.a-section > div.a-section > h2 > a > span.a-text-normal::text")
            # # loader.add_css('name',".a-text-normal::text")
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