from flask import Flask, render_template, request
import sqlite3

# Connection
con = sqlite3.connect('restro.db', check_same_thread=False)

# Cursor
cur = con.cursor()

app = Flask(__name__, static_url_path='/static')

stored_variable = ''


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/order_success', methods = ['POST'])
def order_success():
    if request.method == 'POST':
        name = request.form['full_name']
        email = request.form['email_address']
        msgbox = request.form['message']
        return render_template('reservation.html', name=name, email=email, msgbox = msgbox)
    

@app.route('/store_list', methods=['POST'])
def store_list():
    global stored_variable
    list_id = request.form['list_id']  # Get the list_id from the POST request
    stored_variable = list_id  # Store the list_id in the variable
    return render_template('display_id.html', list_id=stored_variable)

@app.route('/display_id')
def display_id():
    global stored_variable
    itemdata = []
    intid = int(stored_variable)
    data = cur.execute("SELECT * FROM fooditems WHERE id = (?)", (intid,))
    for d in data:
        itemdata.append(d)

    #print(data)
    #print(itemdata[0][1])

    item_name = itemdata[0][1]
    item_price = itemdata[0][2]
    return render_template('display_id.html', list_id=stored_variable, typeid=type(stored_variable), data=itemdata, item=item_name, price=item_price)

@app.route('/checkout')
def checkout():
    return render_template("checkout-page.html")

@app.route('/submit', methods=['POST'])
def handle_form_submission():
    return '''
        <script>
        alert('Order Confirmed !');
        window.location.href = '/';  // Redirect back to the homepage or any other page
    </script>'
    '''