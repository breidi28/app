from fhict_cb_01.CustomPymata4 import CustomPymata4
import requests
import time
import serial
from bs4 import BeautifulSoup
import sqlite3

URL = 'http://localhost:5000/dashboard'
DATABASE = 'orders.db'
BUTTON1PIN = 8
BUTTON2PIN = 9

response = requests.post("http://localhost:5000/send_data")
orders = response.json()
orders = orders['orders']

def setup():
    global board
    board = CustomPymata4(com_port="COM7")
    board.displayOn()
    board.set_pin_mode_digital_input_pullup(BUTTON1PIN)
    board.set_pin_mode_digital_input_pullup(BUTTON2PIN)
    return board

times = {
    'pepperoni': 10,
    'cheese': 8,
    'veggie': 6,
    'meat_lovers': 7,
    'vegan': 5,
    'quattro_formaggi': 9,
    'quattro_stagioni': 11,
    'supreme': 7,
    'tonno': 8
}
counts = {}
for order in orders:
    for pizza_type in times.keys():
        if order[pizza_type] != '0':
            if pizza_type not in counts:
                counts[pizza_type] = 0
            counts[pizza_type] += 1

times_per_pizza = {}
for pizza_type, count in counts.items():
    times_per_pizza[pizza_type] = count * times[pizza_type]

def loop():
    count_nr_pizzas = 0
    for pizza_type, time_sec in times_per_pizza.items():
        count_nr_pizzas += 1
    for pizza_type, time_sec in times_per_pizza.items():
        board.displayShow(pizza_type)
        time.sleep(2)
        board.displayShow(str(time_sec))
        time.sleep(2)
        level1 = board.digital_read(BUTTON1PIN)[0]
        while level1 == 1:
            level1 = board.digital_read(BUTTON1PIN)[0]
            time.sleep(0.01)
        if level1 == 0:
                while time_sec > 0:
                    board.displayShow(str(time_sec))
                    time.sleep(1)
                    time_sec -= 1
                time.sleep(1)
        
                
    board.displayShow('done')
    time.sleep(1)
    #update the database
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("UPDATE orders SET status = 'ready' WHERE status = 'pending'")
    conn.commit()
    conn.close()
    board.displayOff()
        

if __name__ == '__main__':
    setup()
    loop()
