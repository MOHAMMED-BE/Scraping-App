# from crypt import methods
import atexit
# from concurrent.futures import thread
from datetime import datetime
# from distutils.log import debug
# from email.policy import default
import json
import os
import subprocess
# import threading
from turtle import title
import MySQLdb
# from colorama import Cursor
from flask import Flask, redirect,render_template, session,url_for, request,flash,copy_current_request_context
# import flask
from flask_mysqldb import MySQL
from classes.dotDict import dotdict
from forms import LoginForm, RegistrationForm,ScrapingForm
# from flask_wtf import FlaskForm
# from scrapy.crawler import CrawlerProcess
from  flask_session import Session
import numpy as np
# from jumiaSpider import getJumiaProducts as getJumiaProducts
app = Flask(__name__)



app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '' #nfakira
app.config['MYSQL_DB'] = 'FlaskAppDB'

# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "memcached"
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "9adda8bf738de307aea09ba4faebcb19140a6223"

# Session(app)
sess = Session()
sess.init_app(app)
mysql = MySQL(app)


# app.config['SECRET_KEY'] = '9adda8bf738de307aea09ba4faebcb19140a6223'


jumiaData  = {}
amazonData = {}
jumiaNameList  = []
jumiaPriceList = []
jumiaImageList = []


def get_results(db_cursor):
    desc = [d[0] for d in db_cursor.description]
    results = [dotdict(dict(zip(desc, res))) for res in db_cursor.fetchall()]
    return results

# -----------------------------------------------------------------
# -- home                                                    --
# -----------------------------------------------------------------

@app.route("/")
@app.route("/home")
def home():
    from classes.Functions import getJumiaProducts,getPriceFromJumia

    form = ScrapingForm()

    # filename = os.path.join(app.static_folder, 'data/data.json')
    with open("jumiaDataScraping.json","r") as jumiaFile:
        jumiaData = json.load(jumiaFile)
    
    with open("amazonDataScraping.json","r") as amazonFile:
        amazonData = json.load(amazonFile)


    JumiaProducts = getJumiaProducts()

    
    
    for i in jumiaData[JumiaProducts]['name']:
        jumiaNameList.append(i)
        
    
    # for i,j in zip(jumiaData[JumiaProducts]['price'],range(5)):
    #     i = getPriceFromJumia(i)
    #     maxValue = i
    #     jumiaPriceList.append(i)
    #     if j == 0:
    #         break

    for i in jumiaData[JumiaProducts]['price']:
        i = getPriceFromJumia(i)
        jumiaPriceList.append(i)

    for i in jumiaData[JumiaProducts]['image']:
        jumiaImageList.append(i)

    # jumiaPriceList = list(map(lambda x: x.replace(',', ''), jumiaPriceList))

    name = jumiaNameList[0]
    price = jumiaPriceList[0]
    image = jumiaImageList[0]
    # price = max(jumiaPriceList)

    # lessons = get_results(cursor)
    # lessons = cursor.fetchall()

    return render_template("home.html", title="BMS SCRIPER" ,
    jumiaData = jumiaData[JumiaProducts],
    jumiaNameList = jumiaNameList,
    # price = jumiaPriceList,
    image = jumiaImageList,
    name = JumiaProducts,
    price = price,
    form=form
    )

@app.route("/about")
def about():
    return render_template("about.html", title="About")

# -----------------------------------------------------------------
# -- register                                                    --
# -----------------------------------------------------------------

@app.route("/register" , methods=['GET','POST'])
def registration():
    form = RegistrationForm()
    return render_template('register.html' , title='register', form = form )

# -----------------------------------------------------------------
# -- login                                                    --
# -----------------------------------------------------------------

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email     = request.form['email']
        password  = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password,))
        # user = get_results(cursor)
        user = cursor.fetchone()

        cursor.close()

        if form.validate_on_submit():
            if user:
                flash(f"user {user['username']} connected",'success')
            else:
                flash(f"email or password not correct",'danger')

    return render_template('login.html' , title='login', form = form)


# -----------------------------------------------------------------
# -- insert                                                    --
# -----------------------------------------------------------------

@app.route("/insert" , methods=['POST'])
def insert():
    form = RegistrationForm()
    if request.method == 'POST':
        fname     = request.form['fname']
        lname     = request.form['lname']
        username  = request.form['username']
        email     = request.form['email']
        password  = request.form['password']
        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users VALUES(%s,%s,%s,%s,%s)',(fname,lname,username,email,password))
        mysql.connection.commit()
        cursor.close()
    if form.validate_on_submit():
        flash(f"user created successfully",'success')
        return redirect(url_for('registration'))







# ---------------------------------------------------
#  Scraping
# ---------------------------------------------------


# product_name = ""
@app.route('/scrape' , methods=['POST','GET'])
def scrape():
    from classes.Functions import get_flask_env, teardown

    # from jumia import jumia

    # process = CrawlerProcess()
    # process.crawl(jumia)
    # process.start() 

    # a = jumia()
    # # a.run()

    # jumia.run()

    # varx = 'redmi note 10 pro'

    # scrape.product_name = ""

    

    # global product_name 

     


    flask_env = get_flask_env()
    # the command to start app.py, would be: flask run --host 0.0.0.
    # command.append(python_command)
    
    # i = 0

    # if i == 0:
    # command.append("cd")
    # command.append("webapp")
    # monitor = subprocess.Popen(command, env=flask_env)
    # atexit.register(teardown, monitor)
    # @copy_current_request_context
    
    # def fun():
    # with app.request_context(environ):
    # form = ScrapingForm()
    # from flask import request
    if request.method == "POST":
        # scrape.product_name = request.form.get("product_name")
        product_name = request.form['product_name']
        id = np.random.random()
        # now = datetime.now()
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # product_name = scrape.product_name
        session['product_name'] = request.form.get("product_name")
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO product VALUES(%s,%s,%s,%s,%s)',(id,product_name,"img","user",date))
        # cursor.execute('INSERT INTO product VALUES(%s,%s,%s,%s,%s)',(id,product_name,"img","user",date))
        mysql.connection.commit()
        cursor.close()


        def run():
            command = []
            command.append("scrapy")
            command.append("runspider")
            command.append("usdToMad.py")
            monitor = subprocess.Popen(command, env=flask_env)
            atexit.register(teardown, monitor)

            command = []
            command.append("scrapy")
            command.append("runspider")
            command.append("jumiaSpider.py")
            monitor = subprocess.Popen(command, env=flask_env)
            atexit.register(teardown, monitor)

            command = []
            command.append("scrapy")
            command.append("runspider")
            command.append("amazonSpider.py")
            monitor = subprocess.Popen(command, env=flask_env)
            atexit.register(teardown, monitor)

        run()

        def delete():
            cursor = mysql.connection.cursor()
            cursor.execute('delete from product where name = %s',(product_name,))
            mysql.connection.commit()
            cursor.close()



        # return redirect(url_for('pro'))

    # return render_template('progressbarV3.html' , title='progressV1')
    return render_template('progressbarV3.html',title="progress"), {"Refresh": "10; url=home"}

# with app.app_context():
#     # scrape()
#     product = session['product_name']


@app.route('/pro')
def pro():


    return render_template('progressbarV3.html' , title='progressV1')
    




















# -----------------------------------------------------------------
# -- sign in                                                    --
# -----------------------------------------------------------------

# @app.route("/select" , methods=['POST'])
# def select():
#     form = LoginForm()
#     if request.method == 'POST':
#         email     = request.form['email']
#         # password  = request.form['password']
        
#         cursor = mysql.connection.cursor()
#         cursor.execute(f"select * from users where email='{email}'")
#         # user = get_results(cursor)
#         user = cursor.fetchall()

#         cursor.close()

#     # if form.validate_on_submit():
#     if user[3] == email: # and user.password == password
#         flash(f"user connected")
    #     return redirect(url_for('login'))
    # else:
    #     flash(f"not connected")
    # return render_template('login.html' , title='login', form = form)











if __name__ == "__main__":
    app.run(debug=True)

 
# app.run(host='localhost', port=9000)





"""
from distutils.log import debug
from flask import Flask,render_template, request
from flask_mysqldb import MySQL
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskDB'
 
mysql = MySQL(app)

# #Creating a connection cursor
# with app.app_context():
#     cursor = mysql.connection.cursor()
 
# #Executing SQL Statements
# # cursor.execute('CREATE TABLE table_name(field1 int, field2 int)')
#     cursor.execute('INSERT INTO Test VALUES(1,"ZZ","DD")')
# # cursor.execute(' DELETE FROM table_name WHERE condition ')
 
# #Saving the Actions performed on the DB
#     mysql.connection.commit()
 
# #Closing the cursor
#     cursor.close()

@app.route('/form')
def form():
    return render_template('form.html')
 
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return "Login via the login Form"
     
    if request.method == 'POST':
        id     = request.form['id']
        name   = request.form['name']
        prenom = request.form['prenom']
        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO Test VALUES(%s,%s,%s)',(id,name,prenom))
        mysql.connection.commit()
        cursor.close()
        return f"Done!!"
 
app.run(host='localhost', port=5000)
"""


# lessons = [
#     {
#         "title": "Request Library Course",
#         "course": "Python",
#         "author": "Omar",
#         "thumbnail": "thumbnail.jpg",
#     },
#     {
#         "title": "Request Library Course",
#         "course": "Python",
#         "author": "Omar",
#         "thumbnail": "thumbnail.jpg",
#     },
#     {
#         "title": "Request Library Course",
#         "course": "Python",
#         "author": "Omar",
#         "thumbnail": "thumbnail.jpg",
#     },
#     {
#         "title": "Request Library Course",
#         "course": "Python",
#         "author": "Omar",
#         "thumbnail": "thumbnail.jpg",
#     },
#     {
#         "title": "Request Library Course",
#         "course": "Python",
#         "author": "Omar",
#         "thumbnail": "thumbnail.jpg",
#     },
#     {
#         "title": "Request Library Course",
#         "course": "Python",
#         "author": "Omar",
#         "thumbnail": "thumbnail.jpg",
#     },
# ]

# courses = [
#     {
#         "name": "Python",
#         "icon": "python.svg",
#         "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Neque quidem nihil dolor officiis at magni!",
#     },
#     {
#         "name": "Data Analysis",
#         "icon": "analysis.png",
#         "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Neque quidem nihil dolor officiis at magni!",
#     },
#     {
#         "name": "Machine Learning",
#         "icon": "machine-learning.png",
#         "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Neque quidem nihil dolor officiis at magni!",
#     },
#     {
#         "name": "Web Design",
#         "icon": "web.png",
#         "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Neque quidem nihil dolor officiis at magni!",
#     },
#     {
#         "name": "Blockchain",
#         "icon": "blockchain.png",
#         "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Neque quidem nihil dolor officiis at magni!",
#     },
#     {
#         "name": "Tips & Tricks",
#         "icon": "idea.png",
#         "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Neque quidem nihil dolor officiis at magni!",
#     },
# ]



