"""
Database setup script for the Food Ordering System
Run this script to create the MySQL database and tables
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_database():
    """Create the MySQL database if it doesn't exist"""
    try:
        # Connect to MySQL server (without specifying database)
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '')
        )
        
        cursor = connection.cursor()
        
        # Create database
        database_name = os.getenv('DB_NAME', 'ordering_system')
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        print(f"Database '{database_name}' created successfully (or already exists)")
        
        # Use the database
        cursor.execute(f"USE {database_name}")
        
        # Create the orders table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS `order` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `order_number` VARCHAR(10) UNIQUE NOT NULL,
            `customer_name` VARCHAR(100) NOT NULL,
            `customer_phone` VARCHAR(20) NULL,
            `order_items` TEXT NOT NULL,
            `total_price` DECIMAL(10, 2) NOT NULL,
            `status` VARCHAR(20) DEFAULT 'pending',
            `order_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
            `completed_time` DATETIME NULL,
            INDEX `idx_status` (`status`),
            INDEX `idx_order_time` (`order_time`),
            INDEX `idx_order_number` (`order_number`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        cursor.execute(create_table_query)
        print("Table 'order' created successfully (or already exists)")
        
        # Insert some sample data for testing (optional)
        sample_data_query = """
        INSERT IGNORE INTO `order` (order_number, customer_name, customer_phone, order_items, total_price, status)
        VALUES 
        ('SAMPLE1', 'John Doe', '+1234567890', 'Margherita Pizza - $16.99; Soda - $2.99', 19.98, 'completed'),
        ('SAMPLE2', 'Jane Smith', NULL, 'BBQ Burger - $14.99; Fresh Lemonade - $3.99', 18.98, 'pending');
        """
        
        cursor.execute(sample_data_query)
        connection.commit()
        print("Sample data inserted successfully")
        
    except Error as e:
        print(f"Error: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

def test_connection():
    """Test the database connection"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'ordering_system')
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM `order`")
            count = cursor.fetchone()[0]
            print(f"Database connection successful! Found {count} orders in the database.")
            
    except Error as e:
        print(f"Error connecting to database: {e}")
        print("Please make sure:")
        print("1. MySQL server is running")
        print("2. Your .env file has the correct database credentials")
        print("3. The database user has proper permissions")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    print("Setting up Food Ordering System Database...")
    print("=" * 50)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("WARNING: .env file not found!")
        print("Please copy .env.example to .env and update the database credentials")
        exit(1)
    
    # Create database and tables
    create_database()
    
    print("\n" + "=" * 50)
    print("Database setup complete!")
    print("Testing connection...")
    test_connection()
    
    print("\nNext steps:")
    print("1. Make sure your .env file has correct Twilio credentials (for SMS)")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run the application: python app.py")
