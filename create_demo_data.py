#!/usr/bin/env python3
"""
Demo data script for the Food Ordering System
Adds sample orders for testing and demonstration
"""

import os
from datetime import datetime, timedelta
import random

def create_demo_orders():
    """Create sample orders for demonstration"""
    try:
        from app import app, db, Order
        
        with app.app_context():
            # Check if demo orders already exist
            existing_orders = Order.query.filter(Order.order_number.like('DEMO%')).count()
            if existing_orders > 0:
                print(f"Demo orders already exist ({existing_orders} found)")
                return
            
            # Sample customers and orders
            demo_orders = [
                {
                    'order_number': 'DEMO01',
                    'customer_name': 'John Smith',
                    'customer_phone': '+1234567890',
                    'order_items': 'Margherita Pizza - $16.99; Soda - $2.99',
                    'total_price': 19.98,
                    'status': 'pending'
                },
                {
                    'order_number': 'DEMO02', 
                    'customer_name': 'Sarah Johnson',
                    'customer_phone': None,
                    'order_items': 'BBQ Burger - $14.99; Buffalo Wings (8pc) - $12.99; Fresh Lemonade - $3.99',
                    'total_price': 31.97,
                    'status': 'in_progress'
                },
                {
                    'order_number': 'DEMO03',
                    'customer_name': 'Mike Davis',
                    'customer_phone': '+1987654321',
                    'order_items': 'Chicken Alfredo Pasta - $15.99; Mozzarella Sticks - $8.99',
                    'total_price': 24.98,
                    'status': 'pending'
                },
                {
                    'order_number': 'DEMO04',
                    'customer_name': 'Lisa Chen',
                    'customer_phone': '+1555123456',
                    'order_items': 'Pepperoni Pizza - $18.99; Soda - $2.99',
                    'total_price': 21.98,
                    'status': 'completed',
                    'completed_time': datetime.utcnow() - timedelta(minutes=30)
                }
            ]
            
            created_count = 0
            for order_data in demo_orders:
                # Set order time to recent past
                order_time = datetime.utcnow() - timedelta(minutes=random.randint(5, 60))
                
                order = Order(
                    order_number=order_data['order_number'],
                    customer_name=order_data['customer_name'],
                    customer_phone=order_data.get('customer_phone'),
                    order_items=order_data['order_items'],
                    total_price=order_data['total_price'],
                    status=order_data['status'],
                    order_time=order_time,
                    completed_time=order_data.get('completed_time')
                )
                
                db.session.add(order)
                created_count += 1
            
            db.session.commit()
            print(f"✅ Created {created_count} demo orders successfully!")
            print("   Visit http://localhost:5000/worker to see the orders")
            
    except Exception as e:
        print(f"❌ Failed to create demo orders: {e}")

def main():
    print("🎭 Creating Demo Orders...")
    print("=" * 40)
    
    create_demo_orders()
    
    print("\nDemo orders created! You can now:")
    print("1. Visit the customer interface at http://localhost:5000/")
    print("2. Check the worker dashboard at http://localhost:5000/worker")
    print("3. View order history at http://localhost:5000/order_history")

if __name__ == "__main__":
    main()
