from fhict_cb_01.CustomPymata4 import CustomPymata4
import requests
import time

URL = 'http://localhost:5000/dashboard'
LDRPIN = 2
BUTTON1PIN = 8
BUTTON2PIN = 9

print('Starting up...')

global board
board = CustomPymata4(com_port = "COM8")
board.set_pin_mode_digital_input_pullup(BUTTON1PIN)
board.set_pin_mode_digital_input_pullup(BUTTON2PIN)
board.displayOn()

while True:
    response = requests.get(URL)
    if response.content:
        orders = response.json()
        if len(orders) > 0:
            order = orders[0]
            board.displayClear()
            board.displayPrint(order['name'])
            board.displayPrint('Pepperoni: ' + order['pepperoni'] + ' ' + order['pepperoni_size'])
            board.displayPrint('Mushroom: ' + order['mushroom'] + ' ' + order['mushroom_size'])
            board.displayPrint('Cheese: ' + order['cheese'] + ' ' + order['cheese_size'])
            board.displayPrint('Status: ' + order['status'])
            board.displayPrint('Press button 1 to')
            board.displayPrint('accept order')
            board.displayPrint('Press button 2 to')
            board.displayPrint('reject order')
            board.displayPrint('Press button 1 and 2')
            board.displayPrint('to cancel order')
            # wait for button 1 to be pressed
            while True:
                if board.digital_read(BUTTON1PIN) == 0:
                    # button 1 pressed
                    print('Button 1 pressed')
                    break
                elif board.digital_read(BUTTON2PIN) == 0:
                    # button 2 pressed
                    print('Button 2 pressed')
                    break
                time.sleep(0.1)
            # wait for button 1 and 2 to be pressed
            while True:
                if board.digital_read(BUTTON1PIN) == 0 and board.digital_read(BUTTON2PIN) == 0:
                    # button 1 and 2 pressed
                    print('Button 1 and 2 pressed')
                    break
                time.sleep(0.1)
            # wait for button 1 and 2 to be released
            while True:
                if board.digital_read(BUTTON1PIN) == 1 and board.digital_read(BUTTON2PIN) == 1:
                    # button 1 and 2 released
                    print('Button 1 and 2 released')
                    break
                time.sleep(0.1)
            # send request to update order status
            if board.digital_read(BUTTON1PIN) == 0:
                # button 1 pressed
                requests.post('http://localhost:5000/dashboard', json={'id': order['id'], 'status': 'accepted'})
            elif board.digital_read(BUTTON2PIN) == 0:
                # button 2 pressed
                requests.post('http://localhost:5000/dashboard', json={'id': order['id'], 'status': 'rejected'})
            else:
                # button 1 and 2 pressed
                requests.post('http://localhost:5000/dashboard', json={'id': order['id'], 'status': 'cancelled'})
        else:
            board.displayClear()
            board.displayPrint('No orders')
            board.displayPrint('available')
            time.sleep(1)
    else:
        board.displayClear()
        board.displayPrint('No orders')
        board.displayPrint('available')
        time.sleep(1)

    time.sleep(0.1)


