from flask import Flask, render_template, jsonify
from flask_pymongo import PyMongo
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/ordering_system')
mongo = PyMongo(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

@app.route('/')
def display():
    """Public display page showing order status"""
    return render_template('display.html')

@app.route('/api/display/orders')
def get_display_orders():
    """API endpoint to get orders for display"""
    # Get all orders that are not completed or completed within last 5 minutes
    five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)
    
    orders = list(mongo.db.orders.find({
        '$or': [
            {'status': {'$in': ['pending', 'in_progress']}},
            {
                'status': 'completed',
                'completed_time': {'$gte': five_minutes_ago}
            }
        ]
    }).sort('order_time', 1))
    
    orders_data = []
    for order in orders:
        # Determine time info
        time_info = ''
        if order.get('order_time'):
            elapsed = (datetime.utcnow() - order['order_time']).total_seconds() / 60
            time_info = f"{int(elapsed)} min ago"
        
        orders_data.append({
            'id': str(order['_id']),
            'order_number': order['order_number'],
            'customer_name': order['customer_name'],
            'order_items': order['order_items'],
            'status': order['status'],
            'time_info': time_info
        })
    
    return jsonify(orders_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
