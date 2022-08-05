from datetime import datetime
import json
import os
from flask import  session
from app import mysql

class dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def getProductName():
        data = {}
        with open("ProductName.json","r") as jumiaFile:
            data = json.load(jumiaFile)
        ProductName = data['product_name']
        return ProductName


char_to_replace = {','  : '',' '  : '','.00': '','Dhs': ''}

def getPriceFromJumia(arg):
    for key, value in char_to_replace.items():
        arg = arg.replace(key, value)
    return float(arg)


def get_flask_env():
    flask_env = os.environ.copy()
    if "FLASK_APP" not in flask_env:
        flask_env["env"] = "./app.py"
    if "FLASK_ENV" not in flask_env:
        flask_env["FLASK_ENV"] = "development"
    return flask_env

def teardown(process_handle):
    process_handle.terminate() 
    process_handle.wait()

def delete():
    cursor = mysql.connection.cursor()
    cursor.execute('delete from search')
    mysql.connection.commit()
    cursor.close()


def addToProduct():
    with open("jumiaDataScraping.json","r") as jumiaFile:
        jumiaData = json.load(jumiaFile)
    
    with open("amazonDataScraping.json","r") as amazonFile:
        amazonData = json.load(amazonFile)

    with open("currencyScrapingData.json","r") as currencyFile:
        currencyData = json.load(currencyFile)

    scrapingDate = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    if session['product_name']:
        name  = session['product_name']

    jumiaPrice =  jumiaData['price']
    jumiaPrice = getPriceFromJumia(jumiaPrice)

    currency    = currencyData['currency']['currency']
    amazonPrice = amazonData['price']
    amazonPrice =  amazonPrice * currency

    image    = jumiaData['image']
    username = session['username']


    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO products(name,image,username,jumiaPrice,amazonPrice,scrapingDate) VALUES(%s,%s,%s,%s,%s,%s)',(name,image,username,jumiaPrice,amazonPrice,scrapingDate,))
    mysql.connection.commit()
    cursor.close()
