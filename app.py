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

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/mario', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        name = request.form.get('name')
        pepperoni = request.form.get('pepperoni')
        cheese = request.form.get('cheese')
        veggie = request.form.get('veggie')
        meat_lovers = request.form.get('meat_lovers')
        vegan = request.form.get('vegan')
        quattro_formaggi = request.form.get('quattro_formaggi')
        quattro_stagioni = request.form.get('quattro_stagioni')
        supreme = request.form.get('supreme')
        tonno = request.form.get('tonno')
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO orders (name, pepperoni, cheese, veggie, meat_lovers, vegan, quattro_formaggi, quattro_stagioni, supreme, tonno, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (name, pepperoni, cheese, veggie, meat_lovers, vegan, quattro_formaggi, quattro_stagioni, supreme, tonno, 'pending'))
        conn.commit()
        cursor.close()
        return render_template('order.html', name=name)
    else:
        return render_template('mario.html')
        
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
        cursor.execute('CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, pepperoni TEXT, cheese TEXT, veggie TEXT, meat_lovers TEXT, vegan TEXT, quattro_formaggi TEXT, quattro_stagioni TEXT, supreme TEXT, tonno TEXT, status TEXT)')
        db.commit()
    app.run(debug=True)