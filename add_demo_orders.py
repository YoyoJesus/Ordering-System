#!/usr/bin/env python3
"""
Add more demo orders to MySQL database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Order
from datetime import datetime, timedelta
import random

def add_demo_orders():
    """Add demo orders to the database"""
    with app.app_context():
        # Check if demo orders already exist
        existing_demo = Order.query.filter(Order.order_number.like('DEMO%')).count()
        
        new_orders = [
            {
                'order_number': f'DEMO{existing_demo + 1:02d}',
                'customer_name': 'Alice Brown',
                'customer_phone': '+1555987654',
                'order_items': 'Margherita Pizza - $16.99; Mozzarella Sticks - $8.99; Soda - $2.99',
                'total_price': 28.97,
                'status': 'pending'
            },
            {
                'order_number': f'DEMO{existing_demo + 2:02d}',
                'customer_name': 'Bob Wilson',
                'customer_phone': None,
                'order_items': 'BBQ Burger - $14.99; Fresh Lemonade - $3.99',
                'total_price': 18.98,
                'status': 'in_progress'
            },
            {
                'order_number': f'DEMO{existing_demo + 3:02d}',
                'customer_name': 'Emma Davis',
                'customer_phone': '+1444555666',
                'order_items': 'Pepperoni Pizza - $18.99; Buffalo Wings (8pc) - $12.99',
                'total_price': 31.98,
                'status': 'pending'
            }
        ]
        
        created_count = 0
        for order_data in new_orders:
            # Check if this order number already exists
            if Order.query.filter_by(order_number=order_data['order_number']).first():
                continue
                
            # Create order with recent timestamp
            order_time = datetime.utcnow() - timedelta(minutes=random.randint(5, 45))
            
            order = Order(
                order_number=order_data['order_number'],
                customer_name=order_data['customer_name'],
                customer_phone=order_data.get('customer_phone'),
                order_items=order_data['order_items'],
                total_price=order_data['total_price'],
                status=order_data['status'],
                order_time=order_time
            )
            
            db.session.add(order)
            created_count += 1
        
        if created_count > 0:
            db.session.commit()
            print(f"✅ Added {created_count} new demo orders!")
        else:
            print("ℹ️  Demo orders already exist")
        
        # Show current order count
        total_orders = Order.query.count()
        pending_orders = Order.query.filter_by(status='pending').count()
        in_progress_orders = Order.query.filter_by(status='in_progress').count()
        
        print(f"📊 Database Statistics:")
        print(f"   Total Orders: {total_orders}")
        print(f"   Pending: {pending_orders}")
        print(f"   In Progress: {in_progress_orders}")
        
        return created_count

if __name__ == "__main__":
    print("🎭 Adding Demo Orders to MySQL Database...")
    print("=" * 50)
    
    try:
        count = add_demo_orders()
        
        if count > 0:
            print(f"\n✨ Successfully added {count} orders!")
            print("🌐 Visit http://localhost:5000/worker to see them")
        else:
            print("\n📝 Database already has demo data")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure the Flask app is running and database is accessible")
