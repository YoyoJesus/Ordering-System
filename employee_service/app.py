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

@app.route('/display')
def display_board():
    """Public display board showing all active orders with color coding"""
    return render_template('display_board.html')

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
    # Get pending and in_progress orders, plus recently completed orders (last 10 minutes)
    from datetime import datetime, timedelta
    ten_minutes_ago = datetime.utcnow() - timedelta(minutes=10)
    
    orders = list(mongo.db.orders.find({
        '$or': [
            {'status': {'$in': ['pending', 'in_progress']}},
            {'status': 'completed', 'completed_time': {'$gte': ten_minutes_ago}}
        ]
    }).sort('order_time', 1))
    
    orders_data = []
    for order in orders:
        orders_data.append({
            'id': str(order['_id']),
            'order_number': order['order_number'],
            'customer_name': order['customer_name'],
            'customer_phone': order.get('customer_phone', ''),
            'order_items': order['order_items'],
            'total_price': order['total_price'],
            'status': order['status'],
            'order_time': order['order_time'].isoformat() if 'order_time' in order else None,
            'completed_time': order['completed_time'].isoformat() if 'completed_time' in order else None
        })
    return jsonify(orders_data)

@app.route('/order_history')
def order_history():
    completed_orders = list(mongo.db.orders.find({'status': 'completed'}).sort('completed_time', -1).limit(50))
    for order in completed_orders:
        order['_id'] = str(order['_id'])
    return render_template('order_history.html', orders=completed_orders)

@app.route('/admin/menu')
def admin_menu():
    """Admin page for managing menu items"""
    menu_items = list(mongo.db.menu_items.find().sort([('category', 1), ('name', 1)]))
    # Convert ObjectId to string for JSON serialization
    for item in menu_items:
        item['_id'] = str(item['_id'])
    return render_template('admin_menu.html', menu_items=menu_items)

@app.route('/admin/menu/add', methods=['POST'])
def add_menu_item():
    """Add a new menu item"""
    try:
        name = request.form.get('name')
        category = request.form.get('category')
        description = request.form.get('description', '')
        base_price = float(request.form.get('base_price', 0))
        image_url = request.form.get('image_url', '')
        
        # Parse customizations
        import json
        customizations_json = request.form.get('customizations', '[]')
        customizations = json.loads(customizations_json) if customizations_json else []
        
        menu_item = {
            'name': name,
            'category': category,
            'description': description,
            'base_price': base_price,
            'image_url': image_url,
            'customizations': customizations,
            'active': True,
            'created_at': datetime.utcnow()
        }
        
        mongo.db.menu_items.insert_one(menu_item)
        flash(f'Menu item "{name}" added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding menu item: {str(e)}', 'error')
    
    return redirect(url_for('admin_menu'))

@app.route('/admin/menu/edit/<item_id>', methods=['POST'])
def edit_menu_item(item_id):
    """Edit an existing menu item"""
    try:
        import json
        name = request.form.get('name')
        category = request.form.get('category')
        description = request.form.get('description', '')
        base_price = float(request.form.get('base_price', 0))
        image_url = request.form.get('image_url', '')
        customizations_json = request.form.get('customizations', '[]')
        customizations = json.loads(customizations_json) if customizations_json else []
        
        update_data = {
            'name': name,
            'category': category,
            'description': description,
            'base_price': base_price,
            'image_url': image_url,
            'customizations': customizations,
            'updated_at': datetime.utcnow()
        }
        
        mongo.db.menu_items.update_one(
            {'_id': ObjectId(item_id)},
            {'$set': update_data}
        )
        flash(f'Menu item "{name}" updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating menu item: {str(e)}', 'error')
    
    return redirect(url_for('admin_menu'))

@app.route('/admin/menu/toggle/<item_id>', methods=['POST'])
def toggle_menu_item(item_id):
    """Toggle menu item active status"""
    try:
        item = mongo.db.menu_items.find_one({'_id': ObjectId(item_id)})
        if item:
            new_status = not item.get('active', True)
            mongo.db.menu_items.update_one(
                {'_id': ObjectId(item_id)},
                {'$set': {'active': new_status}}
            )
            status_text = 'activated' if new_status else 'deactivated'
            flash(f'Menu item {status_text} successfully!', 'success')
    except Exception as e:
        flash(f'Error toggling menu item: {str(e)}', 'error')
    
    return redirect(url_for('admin_menu'))

@app.route('/admin/menu/delete/<item_id>', methods=['POST'])
def delete_menu_item(item_id):
    """Delete a menu item"""
    try:
        result = mongo.db.menu_items.delete_one({'_id': ObjectId(item_id)})
        if result.deleted_count > 0:
            flash('Menu item deleted successfully!', 'success')
        else:
            flash('Menu item not found!', 'error')
    except Exception as e:
        flash(f'Error deleting menu item: {str(e)}', 'error')
    
    return redirect(url_for('admin_menu'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
