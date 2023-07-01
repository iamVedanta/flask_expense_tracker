


from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder="templates")

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app)

@app.route("/mainhome")
def mainhome():
    return render_template("mainhomepage.html")


@app.route("/index",methods=['POST'])
def home():
    if request.method == 'POST':
        return render_template("index.html")
    else:
        return render_template("index.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return "Login via the login Form"

    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        # cursor.execute(''' INSERT INTO info_table VALUES(%s,%s)''', (name, password))
        cursor.execute("SELECT name FROM info_table WHERE name='"+name +"' AND password='"+password+"'")
        data = cursor.fetchall()
        print(data)
        cursor.close()
        if len(data) == 0:
            return "Invalid user"
        else:
            return redirect(f'/expensetracker?user={data[0][0]}')
        # mysql.connection.commit()
        # cursor.close()
        # return f"Done!!"

@app.route('/signup', methods=['POST','GET'])
def signuppage():
        error_message = None
        return render_template("signup.html",error_message=error_message)


# @app.route('/expensetracker', methods=['POST', 'GET'])
# def signuppageexpense():
#     error_message = None
#     return render_template("expensetracker.html",error_message)


@app.route('/success')
def success():
    return render_template("successfulsignup.html")


@app.route('/signupsubmit', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return "Login via the login Form"

    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT name FROM info_table WHERE name='" + name + "'")
        loadeddata = cursor.fetchall()

        if len(loadeddata) == 0:
            cursor.execute(''' INSERT INTO info_table VALUES(%s,%s)''', (name, password))
            mysql.connection.commit()
            cursor.close()
            return render_template("successfulsignup.html")
        else:
            return render_template("signup.html",error_message= "User already exists")

@app.route("/add", methods=["POST"])
def add():
    def calculate_total_pages(data, items_per_page):
        # Function to calculate the total number of pages
        # Replace this with your own implementation
        total_items = len(data)
        total_pages = (total_items + items_per_page - 1) // items_per_page
        return total_pages

    error_message= None
    price = request.form["price"]
    category = request.form["category"]
    name = request.form["name"]
    date= request.form["date"]
    print(date)
    if date != None and price != 0:
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO user_details VALUES(%s,%s,%s,%s)''', (name, category, price, date))
        mysql.connection.commit()
    else:
        error_message = "price and date are mandatory"

    cursor.execute("SELECT category,date,price FROM user_details WHERE name='" + name + "'")
    data = cursor.fetchall()
    print(data)
    cursor.close()
    # summing
    column_sum = sum(row[2] for row in data)
    print(column_sum)
    # Pagination parameters
    items_per_page = 5
    current_page = request.args.get('page', 1, type=int)
    print(current_page)
    total_pages = calculate_total_pages(data, items_per_page)

    # Slice data for current page
    start_index = (current_page - 1) * items_per_page
    end_index = start_index + items_per_page
    sliced_data = data[start_index:end_index]
    return render_template("expensetracker.html", expense=data, user=name,error_message= error_message, current_page=current_page , total_pages=total_pages ,column_sum=column_sum)


@app.route('/expensetracker')
def expensetracker():
    def calculate_total_pages(data, items_per_page):
        # Function to calculate the total number of pages
        # Replace this with your own implementation
        total_items = len(data)
        total_pages = (total_items + items_per_page - 1) // items_per_page
        return total_pages

    error_message = None
    current_page = 0
    name = request.args.get('user')
    # name = request.form['name']
    # password = request.form['password']
    cursor = mysql.connection.cursor()
    # cursor.execute(''' INSERT INTO info_table VALUES(%s,%s)''', (name, password))
    cursor.execute("SELECT category,date,price FROM user_details WHERE name='" + name + "'")
    data = cursor.fetchall()
    cursor.close()
    #summing
    column_sum = sum(row[2] for row in data)
    print(column_sum)
    # Pagination parameters
    items_per_page = 5
    current_page = request.args.get('page', 1, type=int)
    print(current_page)
    total_pages = calculate_total_pages(data, items_per_page)

    # Slice data for current page
    start_index = (current_page - 1) * items_per_page
    end_index = start_index + items_per_page
    sliced_data = data[start_index:end_index]

    return render_template("expensetracker.html", expense=sliced_data,user = name,error_message= error_message, current_page=current_page, total_pages=total_pages,column_sum=column_sum)

@app.route('/delete', methods=["POST"])
def delete():
    name = request.form['username']
    category = request.form['categorydel']
    price = request.form['pricedel']
    date = request.form['datedel']
    print(category)
    print(price)
    print(date)
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM user_details WHERE category='"+category+"' AND price='"+price+"' AND date='"+date+"'")
    mysql.connection.commit()
    cursor.close()
    print(name)
    return redirect('/expensetracker?user='+ name +'&page=1')


app.run(host='localhost', port=5000)
