# Food Ordering System 🍕

A complete two-front-end food ordering system built with Python Flask and MySQL. This system allows customers to place orders and receive SMS notifications, while food workers can manage orders through a dedicated dashboard.

## Features

### Customer Interface
- 🛒 **Easy Ordering**: Browse menu items with prices and place orders
- 📱 **SMS Notifications**: Optional phone number for order status updates
- 🎯 **Order Tracking**: Get unique order numbers for tracking
- 💰 **Real-time Total**: Dynamic price calculation as items are selected

### Worker Interface
- 👩‍🍳 **Order Management**: View all pending and in-progress orders
- ⚡ **Status Updates**: Mark orders as "in progress" or "completed"
- 🔄 **Auto Refresh**: Real-time updates of new orders
- 📊 **Order History**: View completed orders with analytics
- 📱 **Automatic SMS**: Send completion notifications to customers

## Technology Stack

- **Backend**: Python 3.12, Flask 2.3.3
- **Database**: MySQL with SQLAlchemy ORM
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **SMS Service**: Twilio API
- **Environment**: python-dotenv for configuration

## Project Structure

```
Ordering-System/
├── app.py                     # Main Flask application
├── setup_database.py         # Database setup script
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── app/
│   ├── templates/
│   │   ├── customer_order.html      # Customer ordering interface
│   │   ├── worker_dashboard.html    # Worker management interface
│   │   ├── order_confirmation.html  # Order success page
│   │   └── order_history.html       # Completed orders view
│   └── static/
│       └── css/
│           └── style.css            # Custom styles
└── README.md
```

## Installation & Setup

### 1. Prerequisites
- Python 3.8+ installed
- MySQL server running
- Twilio account (for SMS notifications)

### 2. Clone and Setup
```bash
# Clone the repository
git clone https://github.com/YoyoJesus/Ordering-System.git
cd Ordering-System

# Create virtual environment
python -m venv .venv

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Activate virtual environment (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration
```

Update the `.env` file with your settings:
```env
# Database Configuration
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=ordering_system

# Flask Configuration
SECRET_KEY=your-secret-key-change-this-in-production

# Twilio Configuration (for SMS notifications)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
```

### 4. Database Setup
```bash
# Run the database setup script
python setup_database.py
```

This script will:
- Create the MySQL database
- Create the required tables
- Insert sample data for testing
- Test the database connection

### 5. Run the Application
```bash
python app.py
```

The application will be available at:
- **Customer Interface**: http://localhost:5000/
- **Worker Dashboard**: http://localhost:5000/worker
- **Order History**: http://localhost:5000/order_history

## Usage Guide

### For Customers
1. Visit the main page at http://localhost:5000/
2. Enter your name and optionally your phone number
3. Select menu items (prices update automatically)
4. Click "Place Order" to submit
5. Receive confirmation with order number
6. Get SMS notification when order is ready (if phone provided)

### For Workers
1. Access the worker dashboard at http://localhost:5000/worker
2. View all pending and in-progress orders
3. Click "Start Cooking" to mark order as in-progress
4. Click "Mark Complete" when order is ready
5. Customer automatically receives SMS notification
6. Use "Auto Refresh" for real-time order updates
7. View order history and analytics at http://localhost:5000/order_history

## Database Schema

### Orders Table
```sql
CREATE TABLE `order` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `order_number` VARCHAR(10) UNIQUE NOT NULL,
    `customer_name` VARCHAR(100) NOT NULL,
    `customer_phone` VARCHAR(20) NULL,
    `order_items` TEXT NOT NULL,
    `total_price` DECIMAL(10, 2) NOT NULL,
    `status` ENUM('pending', 'in_progress', 'completed') DEFAULT 'pending',
    `order_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `completed_time` DATETIME NULL
);
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Customer ordering interface |
| GET | `/worker` | Worker dashboard |
| GET | `/order_history` | Completed orders view |
| POST | `/place_order` | Submit new order |
| POST | `/update_order_status` | Update order status |
| GET | `/api/orders` | Get orders JSON (for auto-refresh) |

## Customization

### Adding Menu Items
Edit the `customer_order.html` template to add new menu categories and items:

```html
<div class="form-check">
    <input class="form-check-input menu-item" type="checkbox" 
           value="New Item - $XX.XX" data-price="XX.XX" id="newitem1">
    <label class="form-check-label" for="newitem1">
        New Item - $XX.XX
    </label>
</div>
```

### Styling
Modify `app/static/css/style.css` to customize the appearance.

### SMS Messages
Update the SMS message templates in `app.py`:
- Order confirmation message (line ~98)
- Order completion message (line ~130)

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Ensure MySQL server is running
   - Check database credentials in `.env`
   - Verify database user permissions

2. **SMS Not Working**
   - Check Twilio credentials in `.env`
   - Verify Twilio phone number format
   - Ensure sufficient Twilio credits

3. **Import Errors**
   - Activate virtual environment
   - Install all dependencies: `pip install -r requirements.txt`

4. **Port Already in Use**
   - Change port in `app.py`: `app.run(port=5001)`
   - Or kill existing process using port 5000

### Debug Mode
The application runs in debug mode by default. For production:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

## Security Considerations

For production deployment:
1. Change the `SECRET_KEY` in `.env`
2. Use environment variables for sensitive data
3. Enable HTTPS
4. Set up proper database user permissions
5. Use a production WSGI server (e.g., Gunicorn)
6. Implement rate limiting
7. Add input validation and sanitization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section above
- Review the installation steps

---

Built with ❤️ using Flask, MySQL, and Bootstrap
A simple flask &amp; sql project that builds two environments for the purposes of allowing people to make food orders, and have workers see and complete them.
