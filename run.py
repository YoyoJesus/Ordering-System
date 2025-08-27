#!/usr/bin/env python3
"""
Quick setup and start script for the Food Ordering System
This script will create database tables and start the Flask application
"""

import os
import sys
from datetime import datetime

def print_banner():
    print("=" * 60)
    print("🍕 Food Ordering System Setup & Start 🍕")
    print("=" * 60)
    print()

def check_environment():
    """Check if .env file exists and warn if Twilio is not configured"""
    if not os.path.exists('.env'):
        print("⚠️  WARNING: .env file not found!")
        print("   Creating basic .env file...")
        # Create basic .env file
        with open('.env', 'w') as f:
            f.write("""# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=ordering_system

# Flask Configuration
SECRET_KEY=dev-secret-key-change-for-production

# Twilio Configuration (for SMS notifications)
# Sign up at https://www.twilio.com to get these credentials
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=
""")
        print("   ✅ Basic .env file created")
        print("   📝 Please edit .env file with your MySQL credentials")
        print()

def create_database_tables():
    """Create database tables using SQLAlchemy"""
    print("📊 Setting up database...")
    try:
        from app import app, db
        with app.app_context():
            db.create_all()
            print("   ✅ Database tables created successfully")
            return True
    except Exception as e:
        print(f"   ❌ Database setup failed: {e}")
        print("   💡 Make sure MySQL is running and credentials in .env are correct")
        return False

def start_application():
    """Start the Flask application"""
    print("🚀 Starting Flask application...")
    print()
    print("🌐 Application URLs:")
    print("   Customer Interface: http://localhost:5000/")
    print("   Worker Dashboard:   http://localhost:5000/worker")
    print("   Order History:      http://localhost:5000/order_history")
    print()
    print("💡 Tips:")
    print("   - Use Ctrl+C to stop the server")
    print("   - Enable auto-refresh in worker dashboard for real-time updates")
    print("   - Configure Twilio in .env for SMS notifications")
    print()
    print("=" * 60)
    
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Application failed to start: {e}")

def main():
    print_banner()
    
    # Check environment
    check_environment()
    
    # Setup database
    if not create_database_tables():
        print("\n❌ Setup failed. Please check the error messages above.")
        input("Press Enter to exit...")
        sys.exit(1)
    
    print()
    input("📍 Setup complete! Press Enter to start the application...")
    print()
    
    # Start application
    start_application()

if __name__ == "__main__":
    main()
