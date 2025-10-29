from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_pymongo import PyMongo
from datetime import datetime
import os
import random
import string
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/ordering_system')
mongo = PyMongo(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Twilio setup
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
twilio_client = None
if os.getenv('TWILIO_ACCOUNT_SID') and os.getenv('TWILIO_AUTH_TOKEN'):
    try:
        twilio_client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    except Exception as e:
        print(f"Twilio error: {e}")

def generate_order_number():
    while True:
        order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not mongo.db.orders.find_one({'order_number': order_number}):
            return order_number

def send_sms(phone_number, message):
    if not twilio_client:
        print(f"SMS would be sent to {phone_number}: {message}")
        return False
    try:
        if phone_number and TWILIO_PHONE_NUMBER:
            if not phone_number.startswith('+'):
                phone_number = '+1' + phone_number.replace('-', '').replace('(', '').replace(')', '').replace(' ', '')
            twilio_client.messages.create(body=message, from_=TWILIO_PHONE_NUMBER, to=phone_number)
            return True
    except Exception as e:
        print(f"SMS sending failed: {e}")
        return False

@app.route('/')
def index():
    # Get all active menu items from database
    menu_items = list(mongo.db.menu_items.find({'active': True}).sort('category', 1))
    return render_template('customer_order.html', menu_items=menu_items)

@app.route('/api/menu_items')
def get_menu_items():
    """API endpoint to get menu items"""
    menu_items = list(mongo.db.menu_items.find({'active': True}).sort('category', 1))
    for item in menu_items:
        item['_id'] = str(item['_id'])
    return jsonify(menu_items)

@app.route('/place_order', methods=['POST'])
def place_order():
    try:
        customer_name = request.form.get('customer_name')
        customer_phone = request.form.get('customer_phone', '').strip()
        
        # Parse the order items from JSON
        import json
        order_items_data = json.loads(request.form.get('order_items', '[]'))
        
        # Calculate total and format items
        total_price = 0
        order_items_text = []
        
        for item in order_items_data:
            item_total = item['price'] * item['quantity']
            total_price += item_total
            
            # Format item with customizations
            item_text = f"{item['quantity']}x {item['name']}"
            if item.get('customizations'):
                item_text += f" ({', '.join(item['customizations'])})"
            item_text += f" - ${item_total:.2f}"
            order_items_text.append(item_text)
        
        order_items_str = '; '.join(order_items_text)
        order_number = generate_order_number()
        
        order = {
            'order_number': order_number,
            'customer_name': customer_name,
            'customer_phone': customer_phone if customer_phone else None,
            'order_items': order_items_str,
            'order_items_detailed': order_items_data,  # Store detailed order data
            'total_price': total_price,
            'status': 'pending',
            'order_time': datetime.utcnow()
        }
        
        mongo.db.orders.insert_one(order)
        
        if customer_phone:
            message = f"Thank you {customer_name}! Your order #{order_number} has been placed. Total: ${total_price:.2f}. We'll text you when it's ready!"
            send_sms(customer_phone, message)
        
        return render_template('order_confirmation.html', 
                             order_number=order_number, 
                             customer_name=customer_name,
                             customer_phone=customer_phone,
                             order_items=order_items_str,
                             total_price=total_price)
    except Exception as e:
        print(f"Error placing order: {str(e)}")
        flash(f'Error placing order: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/orders', methods=['GET'])
def list_orders():
    orders = list(mongo.db.orders.find({'status': {'$in': ['pending', 'in_progress']}}))
    for order in orders:
        order['_id'] = str(order['_id'])
        order['order_time'] = order['order_time'].isoformat() if 'order_time' in order else None
    return jsonify(orders)

# ...existing code...
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
