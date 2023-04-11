from flask import Flask, render_template, request, g
import requests
import csv
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'orders.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_db(error):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        pepperoni = request.form.get('pepperoni')
        pepperoni_size = request.form.get('pepperoni_size')
        mushroom = request.form.get('mushroom')
        mushroom_size = request.form.get('mushroom_size')
        cheese = request.form.get('cheese')
        cheese_size = request.form.get('cheese_size')
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO orders (name, pepperoni, pepperoni_size, mushroom, mushroom_size, cheese, cheese_size, status)
                          VALUES (?, ?, ?, ?, ?, ?, ?, "pending")''', 
                       (name, pepperoni, pepperoni_size, mushroom, mushroom_size, cheese, cheese_size))
        conn.commit()
        cursor.close()
        return render_template('order.html', name=name)
    else:
        return render_template('index.html')
        
@app.route('/dashboard')
def dashboard():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE status = "pending"')
    orders = cursor.fetchall()
    cursor.close()
    return render_template('dashboard.html', orders=orders)

@app.route('/client_dashboard')
def client_dashboard():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders')
    orders = cursor.fetchall()
    cursor.close()
    return render_template('client_dashboard.html', orders=orders)

if __name__ == '__main__':
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, pepperoni TEXT, pepperoni_size TEXT, mushroom TEXT, mushroom_size TEXT, cheese TEXT, cheese_size TEXT, status TEXT DEFAULT "pending")')
        db.commit()
    app.run(debug=True)