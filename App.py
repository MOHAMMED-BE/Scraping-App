from asyncio.windows_events import NULL
import atexit
import json
import subprocess
import MySQLdb
from flask import Flask, redirect,render_template, session,url_for, request,flash
from flask_mysqldb import MySQL
from forms import LoginForm, RegistrationForm,ScrapingForm,deleteProductForm
from  flask_session import Session



app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '' #nfakira
app.config['MYSQL_DB'] = 'FlaskAppDB'
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "9adda8bf738de307aea09ba4faebcb19140a6223"

# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "memcached"

# Session(app)
sess = Session()
sess.init_app(app)
mysql = MySQL(app)



def get_results(db_cursor):
    from classes.Functions import dotdict
    desc = [d[0] for d in db_cursor.description]
    results = [dotdict(dict(zip(desc, res))) for res in db_cursor.fetchall()]
    return results

# -----------------------------------------------------------------
# -- home                                                    --
# -----------------------------------------------------------------

@app.route("/")
@app.route("/home")
def home():

    form = ScrapingForm()
    FormDelete = deleteProductForm()
    
    # for i,j in zip(jumiaData[JumiaProducts]['price'],range(5)):

    products = ""
    if session.get("username") != None:
        username = session['username']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM products where username = %s',(username,))
        products = get_results(cursor)


    return render_template("home.html", title="BMS SCRIPER" ,
    products = products,
    form=form,
    FormDelete =FormDelete
    )

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
        user = cursor.fetchone()

        cursor.close()

        if form.validate_on_submit():
            if user:
                flash(f"user {user['username']} connected",'success')
                session['username'] = user['username']
                return  redirect(url_for('home'))

            else:
                flash(f"email or password not correct",'danger')

    return render_template('login.html' , title='login', form = form)


# -----------------------------------------------------------------
# -- insert user information                                                 --
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
        return redirect(url_for('home'))
    return redirect(url_for('home'))


# ---------------------------------------------------
#  Scraping Data
# ---------------------------------------------------


@app.route('/scraping' , methods=['POST','GET'])
def scraping():
    from classes.Functions import get_flask_env, teardown

    flask_env = get_flask_env()

    if session.get("username") == None:
        return redirect(url_for('login'))

    else:
        if request.method == "POST":
            product_name = request.form['product_name']
            data = {}

            data = {
                "product_name":product_name
            }

            with open("productName.json", 'w') as file:
                json.dump(data, file)
            session['product_name'] = product_name

            def run():
                command = []
                command.append("scrapy")
                command.append("runspider")
                command.append("currencySpider.py")
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
           
    return render_template('progressbar.html'), {"Refresh": "6; url=insertProducts"}


@app.route('/insertProducts' )
def insertProducts():

    from classes.Functions import insertProduct
    insertProduct()

    return redirect(url_for('home'))



@app.route('/deleteProduct/<string:productId>' , methods=['POST','GET'])
def deleteProduct(productId):

    cursor = mysql.connection.cursor()
    cursor.execute('delete from products where id = %s',(productId,))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session['username'] = NULL
    return redirect(url_for('home'))


    




















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



