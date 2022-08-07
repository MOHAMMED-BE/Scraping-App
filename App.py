import atexit
import json
import subprocess
import MySQLdb
from flask import Flask, redirect,render_template, session,url_for, request,flash
from flask_mysqldb import MySQL
from forms import LoginForm, RegistrationForm,ScrapingForm,deleteProductForm
from  flask_session import Session

app = Flask(__name__)

# -----------------------------------------------------------------
# --  Session, DB Configuration
# -----------------------------------------------------------------

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '' 
app.config['MYSQL_DB'] = 'FlaskAppDB'
app.config["SESSION_TYPE"] = "filesystem"
mysql = MySQL(app)
app.secret_key = "9adda8bf738de307aea09ba4faebcb19140a6223"
sess = Session()
sess.init_app(app)



def get_results(db_cursor):
    from classes.Functions import dotdict
    desc = [d[0] for d in db_cursor.description]
    results = [dotdict(dict(zip(desc, res))) for res in db_cursor.fetchall()]
    return results

# -----------------------------------------------------------------
# -- home                                                    
# -----------------------------------------------------------------

@app.route("/")
@app.route("/home")
def home():

    form = ScrapingForm()
    FormDelete = deleteProductForm()
    
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
# -- register                                                    
# -----------------------------------------------------------------

@app.route("/register" , methods=['GET','POST'])
def registration():
    form = RegistrationForm()
    
    return render_template('register.html' , title='register', form = form )


# -----------------------------------------------------------------
# -- login                                                   
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
                flash(f"connected successfully",'success')
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
    if request.method == 'POST' and 'email' in request.form and 'username' in request.form and 'password' in request.form:
        
        username  = request.form['username']
        email     = request.form['email']
        password  = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s or username = %s', (email, username,))
        user = cursor.fetchone()
        cursor.close()

        if form.validate_on_submit():
            if user:
                flash(f"email or username already exist",'warning') #{user.username}
                return  redirect(url_for('registration'))
            else:
                cursor = mysql.connection.cursor()
                cursor.execute('INSERT INTO users VALUES(%s,%s,%s)',(username,email,password,))
                mysql.connection.commit()
                cursor.close()

                flash(f"Your account has been created successfully",'success')
                return  redirect(url_for('home'))

    return redirect(url_for('home'))


# -----------------------------------------------------------------
#  Scraping Data
# -----------------------------------------------------------------

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
           
    return render_template('progressbar.html'), {"Refresh": "6.4; url=insertProducts"}



# -----------------------------------------------------------------
# -- insert product to DB                                                    
# -----------------------------------------------------------------

@app.route('/insertProducts' )
def insertProducts():

    from classes.Functions import insertProduct
    insertProduct()

    return redirect(url_for('home'))


# -----------------------------------------------------------------
# -- delete product from DB                                                    
# -----------------------------------------------------------------

@app.route('/deleteProduct/<string:productId>' , methods=['POST','GET'])
def deleteProduct(productId):

    cursor = mysql.connection.cursor()
    cursor.execute('delete from products where id = %s',(productId,))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('home'))


# -----------------------------------------------------------------
# -- logout                                                  
# -----------------------------------------------------------------

@app.route('/logout')
def logout():
    session['username'] = None
    return redirect(url_for('home'))





if __name__ == "__main__":
    app.run(debug=True)
