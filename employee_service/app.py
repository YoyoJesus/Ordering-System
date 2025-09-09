from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_pymongo import PyMongo
from datetime import datetime
import os
from dotenv import load_dotenv
from twilio.rest import Client
from bson.objectid import ObjectId

load_dotenv()
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/ordering_system')
mongo = PyMongo(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
twilio_client = None
if os.getenv('TWILIO_ACCOUNT_SID') and os.getenv('TWILIO_AUTH_TOKEN'):
    try:
        twilio_client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    except Exception as e:
        print(f"Twilio error: {e}")

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
    return redirect(url_for('worker_dashboard'))

@app.route('/orders', methods=['GET'])
def list_orders():
    orders = list(mongo.db.orders.find({'status': {'$in': ['pending', 'in_progress']}}))
    for order in orders:
        order['_id'] = str(order['_id'])
        order['order_time'] = order['order_time'].isoformat() if 'order_time' in order else None
    return jsonify(orders)

@app.route('/orders/<order_id>/status', methods=['POST'])
def update_order_status(order_id):
    data = request.get_json(force=True)
    new_status = data.get('status')
    update = {'status': new_status}
    if new_status == 'completed':
        update['completed_time'] = datetime.utcnow()
    result = mongo.db.orders.update_one({'_id': mongo.db.ObjectId(order_id)}, {'$set': update})
    return jsonify({'updated': result.modified_count == 1})

@app.route('/worker')
def worker_dashboard():
    orders = list(mongo.db.orders.find({'status': {'$in': ['pending', 'in_progress']}}).sort('order_time', 1))
    for order in orders:
        order['_id'] = str(order['_id'])
    return render_template('worker_dashboard.html', orders=orders)

@app.route('/update_order_status', methods=['POST'])
def update_order_status_form():
    try:
        order_id = request.form.get('order_id')
        new_status = request.form.get('status')
        order = mongo.db.orders.find_one({'_id': ObjectId(order_id)})
        update = {'status': new_status}
        if new_status == 'completed':
            update['completed_time'] = datetime.utcnow()
            if order and order.get('customer_phone'):
                message = f"Hi {order['customer_name']}! Your order #{order['order_number']} is ready for pickup!"
                send_sms(order['customer_phone'], message)
        mongo.db.orders.update_one({'_id': ObjectId(order_id)}, {'$set': update})
        flash(f"Order #{order['order_number']} status updated to {new_status}", 'success')
    except Exception as e:
        flash(f'Error updating order: {str(e)}', 'error')
    return redirect(url_for('worker_dashboard'))

@app.route('/api/orders')
def api_orders():
    orders = list(mongo.db.orders.find({'status': {'$in': ['pending', 'in_progress']}}).sort('order_time', 1))
    orders_data = []
    for order in orders:
        orders_data.append({
            'id': str(order['_id']),
            'order_number': order['order_number'],
            'customer_name': order['customer_name'],
            'order_items': order['order_items'],
            'total_price': order['total_price'],
            'status': order['status'],
            'order_time': order['order_time'].strftime('%H:%M') if 'order_time' in order else ''
        })
    return jsonify(orders_data)

@app.route('/order_history')
def order_history():
    completed_orders = list(mongo.db.orders.find({'status': 'completed'}).sort('completed_time', -1).limit(50))
    for order in completed_orders:
        order['_id'] = str(order['_id'])
    return render_template('order_history.html', orders=completed_orders)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
