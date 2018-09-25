from flask import render_template
from flaskexample import app
from flaskext.mysql import MySQL
from flask import request
from flask import jsonify
from urllib.parse import unquote

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'price_compare'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
cursor = mysql.connect().cursor()

# Polpulate categories from database
sql_query ="SELECT * FROM category"         
cursor.execute(sql_query)
query_results = cursor.fetchall()
categories = []

for i in range(0,len(query_results)):
    categories.append(dict(id=query_results[i][0], name=query_results[i][1])) 

#Polpulate sub categories from database
sql_query ="SELECT * FROM sub_category"         
cursor.execute(sql_query)
query_results = cursor.fetchall()
sub_categories = []

for i in range(0,len(query_results)):
    sub_categories.append(dict(id=query_results[i][0], name=query_results[i][1],category_id=query_results[i][2]))       

app.secret_key = "development-key"
@app.route('/')
@app.route('/index')
def index():
   user = { 'nickname': 'Arif' } # fake user
   return render_template("index.html",title = 'Home',user = user)

@app.route('/search')
def search_input():
    return render_template("search.html", categories=categories)
@app.route('/result', methods=['GET', 'POST'])
def result():
    #pull 'category id' from input field and store it
    category = unquote(request.args.get('category'))
    #pull 'sub_category' from input field and store it
    sub_category = unquote(request.args.get('sub_category'))
    #just select the sub_category  from the database for the category that the user inputs
    sql_query = "SELECT * FROM rochebros_products WHERE category= '" + category +"' AND  sub_category = '" + sub_category + "'"
    cursor.execute(sql_query)
    query_results = cursor.fetchall()
    print(query_results)
    products = []
    for i in range(0,len(query_results)):
       products.append(dict(name=query_results[i][1], price=query_results[i][2], store=query_results[i][4]))
    the_result = ''
    return render_template("result.html", products = products, categories = categories, the_result = the_result)


@app.route('/get_sub_category/<category>')
def get_sub_category(category):
    #Polpulate sub categories from database
    sql_query ="SELECT * FROM sub_category WHERE category_name = '" + category  +"'"   
    cursor.execute(sql_query)
    query_results = cursor.fetchall()
    sub_categories = []
    for i in range(0,len(query_results)):
       sub_categories.append(dict(id=query_results[i][0], name=query_results[i][1]))

    return jsonify(sub_categories)