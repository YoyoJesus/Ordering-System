#!/usr/bin/env python3
"""
Seed script to populate the database with sample menu items
Run this script after starting the MongoDB container
"""

from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to MongoDB
mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/ordering_system')
client = MongoClient(mongo_uri)
db = client.get_database()

print("🌱 Seeding database with sample menu items...")

# Check if menu items already exist
existing_count = db.menu_items.count_documents({})
if existing_count > 0:
    print(f"   Database already has {existing_count} menu items. Skipping seed.")
    print("   To re-seed, delete all menu items first.")
    client.close()
    exit(0)

print("   No existing menu items found. Adding sample data...")

# Sample menu items
sample_items = [
    {
        'name': 'Classic Burger',
        'category': 'main',
        'description': 'Juicy beef patty with lettuce, tomato, and special sauce',
        'base_price': 12.99,
        'image_url': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400',
        'customizations': [
            {'name': 'Extra Cheese', 'price': 1.50},
            {'name': 'Bacon', 'price': 2.00},
            {'name': 'Avocado', 'price': 1.50},
            {'name': 'No Onions', 'price': 0.00}
        ],
        'active': True,
        'created_at': datetime.utcnow()
    },
    {
        'name': 'Margherita Pizza',
        'category': 'main',
        'description': 'Fresh mozzarella, basil, and tomato sauce on a crispy crust',
        'base_price': 14.99,
        'image_url': 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400',
        'customizations': [
            {'name': 'Extra Cheese', 'price': 2.00},
            {'name': 'Pepperoni', 'price': 2.50},
            {'name': 'Mushrooms', 'price': 1.50},
            {'name': 'Olives', 'price': 1.00}
        ],
        'active': True,
        'created_at': datetime.utcnow()
    },
    {
        'name': 'Caesar Salad',
        'category': 'appetizer',
        'description': 'Crisp romaine lettuce with parmesan, croutons, and Caesar dressing',
        'base_price': 8.99,
        'image_url': 'https://images.unsplash.com/photo-1546793665-c74683f339c1?w=400',
        'customizations': [
            {'name': 'Grilled Chicken', 'price': 3.50},
            {'name': 'Shrimp', 'price': 4.50},
            {'name': 'Extra Parmesan', 'price': 1.00}
        ],
        'active': True,
        'created_at': datetime.utcnow()
    },
    {
        'name': 'Chicken Wings',
        'category': 'appetizer',
        'description': 'Crispy wings tossed in your choice of sauce',
        'base_price': 10.99,
        'image_url': 'https://images.unsplash.com/photo-1608039755401-742074f0548d?w=400',
        'customizations': [
            {'name': 'Buffalo Sauce', 'price': 0.00},
            {'name': 'BBQ Sauce', 'price': 0.00},
            {'name': 'Honey Garlic', 'price': 0.00},
            {'name': 'Extra Spicy', 'price': 0.50}
        ],
        'active': True,
        'created_at': datetime.utcnow()
    },
    {
        'name': 'French Fries',
        'category': 'side',
        'description': 'Crispy golden fries seasoned to perfection',
        'base_price': 4.99,
        'image_url': 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=400',
        'customizations': [
            {'name': 'Cheese Sauce', 'price': 1.50},
            {'name': 'Bacon Bits', 'price': 2.00},
            {'name': 'Cajun Seasoning', 'price': 0.50}
        ],
        'active': True,
        'created_at': datetime.utcnow()
    },
    {
        'name': 'Onion Rings',
        'category': 'side',
        'description': 'Crispy battered onion rings with dipping sauce',
        'base_price': 5.99,
        'image_url': 'https://images.unsplash.com/photo-1639024471283-03518883512d?w=400',
        'customizations': [
            {'name': 'Ranch Dip', 'price': 0.50},
            {'name': 'Spicy Mayo', 'price': 0.50}
        ],
        'active': True,
        'created_at': datetime.utcnow()
    },
    {
        'name': 'Coca-Cola',
        'category': 'drink',
        'description': 'Classic refreshing cola',
        'base_price': 2.99,
        'image_url': 'https://images.unsplash.com/photo-1554866585-cd94860890b7?w=400',
        'customizations': [
            {'name': 'Large', 'price': 1.00},
            {'name': 'Extra Ice', 'price': 0.00},
            {'name': 'No Ice', 'price': 0.00}
        ],
        'active': True,
        'created_at': datetime.utcnow()
    },
    {
        'name': 'Lemonade',
        'category': 'drink',
        'description': 'Fresh-squeezed lemonade',
        'base_price': 3.49,
        'image_url': 'https://images.unsplash.com/photo-1523677011781-c91d1bbe2f9f?w=400',
        'customizations': [
            {'name': 'Large', 'price': 1.00},
            {'name': 'Strawberry', 'price': 0.50},
            {'name': 'Mint', 'price': 0.50}
        ],
        'active': True,
        'created_at': datetime.utcnow()
    },
    {
        'name': 'Chocolate Cake',
        'category': 'dessert',
        'description': 'Rich chocolate cake with chocolate frosting',
        'base_price': 6.99,
        'image_url': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400',
        'customizations': [
            {'name': 'Ice Cream', 'price': 2.00},
            {'name': 'Whipped Cream', 'price': 1.00},
            {'name': 'Extra Chocolate Sauce', 'price': 0.50}
        ],
        'active': True,
        'created_at': datetime.utcnow()
    },
    {
        'name': 'Apple Pie',
        'category': 'dessert',
        'description': 'Warm apple pie with a flaky crust',
        'base_price': 5.99,
        'image_url': 'https://images.unsplash.com/photo-1535920527002-b35e96722eb9?w=400',
        'customizations': [
            {'name': 'Vanilla Ice Cream', 'price': 2.00},
            {'name': 'Caramel Sauce', 'price': 0.50},
            {'name': 'Warmed', 'price': 0.00}
        ],
        'active': True,
        'created_at': datetime.utcnow()
    }
]

# Insert menu items
result = db.menu_items.insert_many(sample_items)
print(f"✅ Successfully added {len(result.inserted_ids)} menu items!")

print("\n📋 Menu items by category:")
for category in ['appetizer', 'main', 'side', 'drink', 'dessert']:
    count = db.menu_items.count_documents({'category': category})
    print(f"   {category.capitalize()}: {count} items")

print("\n✨ Database seeding complete!")
print("   You can now access the customer ordering page and admin menu page")

client.close()
