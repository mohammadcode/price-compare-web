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
'''@app.route('/')
@app.route('/index')
def index():
   user = { 'nickname': 'Mohammad Arifuzzaman' } # fake user
   return render_template("index.html",title = 'Home',user = user)
'''
@app.route('/')
@app.route('/index')
@app.route('/search')
def search_input():
    return render_template("search.html", categories=categories)
@app.route('/result', methods=['GET', 'POST'])
def result():
    #pull 'category id' from input field and store it
    category = unquote(request.args.get('category'))
    #pull 'sub_category' from input field and store it
    sub_category = unquote(request.args.get('sub_category'))
    if len(request.args.get('product_type')) > 0:
        product_type = unquote(request.args.get('product_type'))
        product_type_query = "SELECT * FROM product_type WHERE name= '" + product_type + "'"
        cursor.execute(product_type_query)
        key_words = cursor.fetchone()

    if key_words is None:
        sql_query = "SELECT * FROM products WHERE category = %s AND sub_category = %s"
        cursor.execute(sql_query,(category,sub_category))
    else:
        keyword = "%" + key_words[4] + "%" +key_words[5]
        sql_query = "SELECT * FROM products WHERE category = %s AND sub_category = %s AND name LIKE %s"
        cursor.execute(sql_query,(category,sub_category,keyword))

    #cursor.execute(sql_query)
    query_results = cursor.fetchall()
    
    products = []
    for i in range(0,len(query_results)):
       products.append(dict(name=query_results[i][1], price=query_results[i][2], unit=query_results[i][8], store=query_results[i][4]))
    the_result = ''
    return render_template("result.html", products = products, categories = categories, the_result = the_result)


@app.route('/get_sub_category/<category>')
def get_sub_category(category):
    #Polpulate sub categories from database
    sql_query ="SELECT * FROM sub_category WHERE category_name = '" + category  +"'"    
    try:
        cursor.execute(sql_query)
    except Exception as e:
        print("type error: " + str(e))
    #cursor.execute(sql_query)
    query_results = cursor.fetchall()
    sub_categories = []
    for i in range(0,len(query_results)):
       sub_categories.append(dict(id=query_results[i][0], name=query_results[i][1]))

    return jsonify(sub_categories)

@app.route('/get_product_type/<sub_category>/<category>')
def get_product_type(sub_category,category):
    #Polpulate sub categories from database
    sql_query ="SELECT id , name FROM product_type WHERE category = '" + category  +"' AND sub_category='" + sub_category + "'"    
    try:
        cursor.execute(sql_query)
    except Exception as e:
        print("type error: " + str(e))
    #cursor.execute(sql_query)
    query_results = cursor.fetchall()
    product_types = []
    for i in range(0,len(query_results)):
       product_types.append(dict(id=query_results[i][0], name=query_results[i][1]))

    return jsonify(product_types)