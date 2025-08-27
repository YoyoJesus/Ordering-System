from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv
import random
import string

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration - Use SQLite for easier setup
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ordering_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)

# Twilio configuration
twilio_client = None
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

# Initialize Twilio client only if credentials are provided
if os.getenv('TWILIO_ACCOUNT_SID') and os.getenv('TWILIO_AUTH_TOKEN'):
    try:
        from twilio.rest import Client
        twilio_client = Client(
            os.getenv('TWILIO_ACCOUNT_SID'),
            os.getenv('TWILIO_AUTH_TOKEN')
        )
        print("Twilio client initialized successfully")
    except Exception as e:
        print(f"Failed to initialize Twilio client: {e}")
        twilio_client = None
else:
    print("Twilio credentials not provided - SMS notifications will be disabled")

# Database Models
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(10), unique=True, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=True)
    order_items = db.Column(db.Text, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed
    order_time = db.Column(db.DateTime, default=datetime.utcnow)
    completed_time = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Order {self.order_number}>'

# Helper Functions
def generate_order_number():
    """Generate a unique 6-character order number"""
    while True:
        order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not Order.query.filter_by(order_number=order_number).first():
            return order_number

def send_sms(phone_number, message):
    """Send SMS notification using Twilio"""
    try:
        if not twilio_client:
            print(f"SMS would be sent to {phone_number}: {message}")
            return False
            
        if phone_number and TWILIO_PHONE_NUMBER:
            # Format phone number (add +1 if it doesn't start with +)
            if not phone_number.startswith('+'):
                phone_number = '+1' + phone_number.replace('-', '').replace('(', '').replace(')', '').replace(' ', '')
            
            message_obj = twilio_client.messages.create(
                body=message,
                from_=TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            print(f"SMS sent successfully to {phone_number}")
            return True
    except Exception as e:
        print(f"SMS sending failed: {e}")
        return False

# Routes

@app.route('/')
def index():
    """Customer ordering interface"""
    return render_template('customer_order.html')

@app.route('/worker')
def worker_dashboard():
    """Worker dashboard to manage orders"""
    orders = Order.query.filter(Order.status.in_(['pending', 'in_progress'])).order_by(Order.order_time.asc()).all()
    return render_template('worker_dashboard.html', orders=orders)

@app.route('/place_order', methods=['POST'])
def place_order():
    """Handle new order submission"""
    try:
        customer_name = request.form.get('customer_name')
        customer_phone = request.form.get('customer_phone', '').strip()
        order_items = request.form.get('order_items')
        total_price = float(request.form.get('total_price', 0))

        # Generate unique order number
        order_number = generate_order_number()

        # Create new order
        new_order = Order(
            order_number=order_number,
            customer_name=customer_name,
            customer_phone=customer_phone if customer_phone else None,
            order_items=order_items,
            total_price=total_price
        )

        db.session.add(new_order)
        db.session.commit()

        # Send confirmation SMS if phone number provided
        if customer_phone:
            message = f"Thank you {customer_name}! Your order #{order_number} has been placed. We'll text you when it's ready!"
            send_sms(customer_phone, message)

        return render_template('order_confirmation.html', 
                             order_number=order_number, 
                             customer_name=customer_name)

    except Exception as e:
        flash(f'Error placing order: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/update_order_status', methods=['POST'])
def update_order_status():
    """Update order status (worker interface)"""
    try:
        order_id = request.form.get('order_id')
        new_status = request.form.get('status')

        order = Order.query.get_or_404(order_id)
        order.status = new_status

        if new_status == 'completed':
            order.completed_time = datetime.utcnow()
            
            # Send completion SMS if phone number exists
            if order.customer_phone:
                message = f"Hi {order.customer_name}! Your order #{order.order_number} is ready for pickup!"
                send_sms(order.customer_phone, message)

        db.session.commit()
        flash(f'Order #{order.order_number} status updated to {new_status}', 'success')

    except Exception as e:
        flash(f'Error updating order: {str(e)}', 'error')

    return redirect(url_for('worker_dashboard'))

@app.route('/api/orders')
def api_orders():
    """API endpoint for getting orders (for auto-refresh)"""
    orders = Order.query.filter(Order.status.in_(['pending', 'in_progress'])).order_by(Order.order_time.asc()).all()
    orders_data = []
    
    for order in orders:
        orders_data.append({
            'id': order.id,
            'order_number': order.order_number,
            'customer_name': order.customer_name,
            'order_items': order.order_items,
            'total_price': order.total_price,
            'status': order.status,
            'order_time': order.order_time.strftime('%H:%M')
        })
    
    return jsonify(orders_data)

@app.route('/order_history')
def order_history():
    """View completed orders"""
    completed_orders = Order.query.filter_by(status='completed').order_by(Order.completed_time.desc()).limit(50).all()
    return render_template('order_history.html', orders=completed_orders)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
        
        # Add some demo data if the database is empty
        if Order.query.count() == 0:
            demo_orders = [
                Order(
                    order_number='DEMO01',
                    customer_name='John Smith',
                    customer_phone='+1234567890',
                    order_items='Margherita Pizza - $16.99; Soda - $2.99',
                    total_price=19.98,
                    status='pending'
                ),
                Order(
                    order_number='DEMO02',
                    customer_name='Sarah Johnson',
                    order_items='BBQ Burger - $14.99; Buffalo Wings (8pc) - $12.99',
                    total_price=27.98,
                    status='in_progress'
                ),
                Order(
                    order_number='DEMO03',
                    customer_name='Mike Davis',
                    customer_phone='+1987654321',
                    order_items='Chicken Alfredo Pasta - $15.99',
                    total_price=15.99,
                    status='completed',
                    completed_time=datetime.utcnow()
                )
            ]
            
            for order in demo_orders:
                db.session.add(order)
            
            db.session.commit()
            print("Demo data added to database!")
    
    print("\n" + "="*60)
    print("🍕 Food Ordering System Started Successfully! 🍕")
    print("="*60)
    print(f"🌐 Customer Interface: http://localhost:5000/")
    print(f"👩‍🍳 Worker Dashboard:   http://localhost:5000/worker")
    print(f"📊 Order History:      http://localhost:5000/order_history")
    print("="*60)
    print("Press Ctrl+C to stop the server")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
