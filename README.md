# Food Ordering System 🍕

A modern microservices-based food ordering system built with Python Flask, MongoDB, and Docker. This system features two separate services: a customer service for placing orders and an employee service for managing and completing orders, with optional SMS notifications.

## Features

### Customer Service
- 🛒 **Easy Ordering**: Browse menu items with prices and place orders
- 📱 **SMS Notifications**: Optional phone number for order status updates
- 🎯 **Order Tracking**: Get unique order numbers for tracking
- 💰 **Real-time Total**: Dynamic price calculation as items are selected

### Employee Service
- 👩‍🍳 **Order Management**: View all pending and in-progress orders
- ⚡ **Status Updates**: Mark orders as "in progress" or "completed"
- 🔄 **Auto Refresh**: Real-time updates of new orders
- 📊 **Order History**: View completed orders with analytics
- 📱 **Automatic SMS**: Send completion notifications to customers

## Technology Stack

- **Architecture**: Microservices
- **Backend**: Python 3.12, Flask 2.3.3
- **Database**: MongoDB 6.0 with PyMongo
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Containerization**: Docker & Docker Compose
- **SMS Service**: Twilio API (optional)
- **Environment**: python-dotenv for configuration

## Project Structure

```
Ordering-System/
├── docker-compose.yml              # Docker orchestration
├── .env.example                    # Environment variables template
├── requirements.txt                # Root dependencies
├── customer_service/               # Customer microservice
│   ├── app.py                     # Customer Flask application
│   ├── Dockerfile                 # Customer service container
│   ├── requirements.txt           # Customer service dependencies
│   ├── templates/
│   │   ├── base.html
│   │   ├── customer_order.html   # Order placement interface
│   │   └── order_confirmation.html
│   └── static/
│       └── css/
│           └── style.css
└── employee_service/              # Employee microservice
    ├── app.py                     # Employee Flask application
    ├── Dockerfile                 # Employee service container
    ├── requirements.txt           # Employee service dependencies
    ├── templates/
    │   ├── base.html
    │   ├── worker_dashboard.html # Order management interface
    │   └── order_history.html    # Analytics and history
    └── static/
        └── css/
            └── style.css
```

## Installation & Setup

### Option 1: Docker (Recommended)

#### Prerequisites
- Docker Desktop installed
- Docker Compose installed
- Twilio account (optional, for SMS notifications)

#### Quick Start
```bash
# Clone the repository
git clone https://github.com/YoyoJesus/Ordering-System.git
cd Ordering-System

# Create environment file (optional, for SMS)
cp .env.example .env
# Edit .env with your Twilio credentials

# Start all services with Docker Compose
docker-compose up --build
```

The application will be available at:
- **Customer Service**: http://localhost:5000/
- **Employee Service**: http://localhost:5001/

To stop the services:
```bash
docker-compose down
```

To stop and remove all data:
```bash
docker-compose down -v
```

### Option 2: Local Development (Without Docker)

#### Prerequisites
- Python 3.8+ installed
- MongoDB server running locally
- Twilio account (optional, for SMS notifications)

#### Setup Steps
```bash
# Clone the repository
git clone https://github.com/YoyoJesus/Ordering-System.git
cd Ordering-System

# Install MongoDB (if not already installed)
# Windows: Download from https://www.mongodb.com/try/download/community
# macOS: brew install mongodb-community
# Linux: sudo apt-get install mongodb

# Start MongoDB service
# Windows: Start MongoDB service from Services
# macOS/Linux: sudo systemctl start mongod

# Create environment file
cp .env.example .env
# Edit .env with your settings
```

Update the `.env` file with your settings:
```env
# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/ordering_system

# Flask Configuration
SECRET_KEY=your-secret-key-change-this-in-production

# Twilio Configuration (optional - for SMS notifications)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
```

#### Run Customer Service
```bash
cd customer_service

# Create virtual environment
python -m venv .venv

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Activate virtual environment (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the service
python app.py
```

#### Run Employee Service (in a separate terminal)
```bash
cd employee_service

# Create virtual environment
python -m venv .venv

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Activate virtual environment (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the service
python app.py
```

The application will be available at:
- **Customer Service**: http://localhost:5000/
- **Employee Service**: http://localhost:5001/

## Usage Guide

### For Customers
1. Visit the customer service at http://localhost:5000/
2. Enter your name and optionally your phone number
3. Select menu items (prices update automatically)
4. Click "Place Order" to submit
5. Receive confirmation with unique order number
6. Get SMS notification when order is ready (if phone provided and Twilio configured)

### For Employees
1. Access the employee dashboard at http://localhost:5001/
2. View all pending and in-progress orders in real-time
3. Click "Start Cooking" to mark order as in-progress
4. Click "Mark Complete" when order is ready
5. Customer automatically receives SMS notification (if configured)
6. Dashboard auto-refreshes for real-time updates
7. View order history and analytics at http://localhost:5001/order_history

## Architecture

This application uses a **microservices architecture**:

### Services
1. **Customer Service** (Port 5000)
   - Handles customer order placement
   - Manages order confirmation
   - Independent deployment and scaling

2. **Employee Service** (Port 5001)
   - Manages order status updates
   - Provides dashboard for workers
   - Order history and analytics

3. **MongoDB** (Port 27017)
   - Shared database for both services
   - Document-based storage for orders
   - Automatic data persistence with Docker volumes

### Benefits
- **Scalability**: Each service can be scaled independently
- **Isolation**: Services can be developed and deployed separately
- **Resilience**: Failure in one service doesn't affect the other
- **Technology Flexibility**: Each service can use different tech stacks if needed

## Database Schema

### Orders Collection (MongoDB)
```javascript
{
  "_id": ObjectId("..."),
  "order_number": "A4K7G2",           // Unique 6-character code
  "customer_name": "John Doe",
  "customer_phone": "+15551234567",   // Optional
  "order_items": "Pizza, Soda",
  "total_price": 15.99,
  "status": "pending",                // pending, in_progress, completed
  "order_time": ISODate("..."),
  "completed_time": ISODate("...")    // Set when status = completed
}
```

## API Endpoints

### Customer Service (Port 5000)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Customer ordering interface |
| POST | `/place_order` | Submit new order |
| GET | `/order_confirmation/<order_number>` | Order confirmation page |

### Employee Service (Port 5001)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Employee dashboard |
| GET | `/order_history` | Completed orders view |
| POST | `/update_order_status` | Update order status |
| GET | `/api/orders` | Get orders JSON (for auto-refresh) |

## Customization

### Adding Menu Items
Edit the `customer_service/templates/customer_order.html` template to add new menu categories and items:

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
- **Customer Service**: Modify `customer_service/static/css/style.css`
- **Employee Service**: Modify `employee_service/static/css/style.css`

### SMS Messages
Update the SMS message templates in both service files:
- **Customer Service** (`customer_service/app.py`): Order confirmation message
- **Employee Service** (`employee_service/app.py`): Order completion message

### Docker Configuration
Edit `docker-compose.yml` to:
- Change port mappings
- Add environment variables
- Adjust resource limits
- Configure MongoDB settings

## Troubleshooting

### Common Issues

1. **Docker Container Won't Start**
   - Ensure Docker Desktop is running
   - Check if ports 5000, 5001, or 27017 are already in use
   - Run `docker-compose down -v` to remove old containers and volumes
   - Run `docker-compose up --build` to rebuild

2. **Cannot Connect to MongoDB**
   - Verify MongoDB container is running: `docker ps`
   - Check MongoDB logs: `docker logs ordering_mongodb`
   - Ensure MONGO_URI is correct in docker-compose.yml

3. **SMS Not Working**
   - Verify Twilio credentials in `.env` file
   - Check Twilio phone number format (+1234567890)
   - Ensure sufficient Twilio account credits
   - Note: SMS is optional - system works without it

4. **Port Already in Use**
   - Check what's using the port: `netstat -ano | findstr :5000` (Windows)
   - Change port mapping in `docker-compose.yml`:
     ```yaml
     ports:
       - "5002:5000"  # Use 5002 instead of 5000
     ```

5. **Changes Not Reflecting**
   - Rebuild containers: `docker-compose up --build`
   - Clear browser cache
   - Ensure you're editing the correct service folder

### Debug Mode
Both services run in development/debug mode by default. For production:
- Set `FLASK_ENV=production` in docker-compose.yml
- Disable debug mode in app.py files
- Use a production WSGI server (e.g., Gunicorn)

### View Logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs customer_service
docker-compose logs employee_service
docker-compose logs mongodb

# Follow logs in real-time
docker-compose logs -f
```

## Security Considerations

For production deployment:
1. **Change the `SECRET_KEY`** in `.env` to a strong, random value
2. **Use environment variables** for all sensitive data (never commit `.env`)
3. **Enable HTTPS** with SSL/TLS certificates
4. **Set up MongoDB authentication** with username/password
5. **Use a production WSGI server** (e.g., Gunicorn, uWSGI)
6. **Implement rate limiting** to prevent abuse
7. **Add input validation and sanitization** to prevent injection attacks
8. **Set `FLASK_ENV=production`** to disable debug mode
9. **Use Docker secrets** for sensitive configuration in production
10. **Implement proper logging** and monitoring
11. **Keep dependencies updated** regularly
12. **Use a reverse proxy** (e.g., Nginx) in front of Flask services

### Production Docker Setup
```yaml
# Use environment variables instead of .env file
environment:
  - SECRET_KEY=${SECRET_KEY}
  - MONGO_URI=mongodb://username:password@mongodb:27017/ordering_system?authSource=admin
  - FLASK_ENV=production
```

## Deployment

### Docker Deployment (Recommended)
1. Set up a cloud VM (AWS, GCP, Azure, DigitalOcean)
2. Install Docker and Docker Compose
3. Clone the repository
4. Configure environment variables
5. Run `docker-compose up -d` for production
6. Set up Nginx as reverse proxy
7. Configure SSL with Let's Encrypt

### Platform-as-a-Service Options
- **Heroku**: Supports Docker containers
- **AWS ECS**: Elastic Container Service
- **Google Cloud Run**: Serverless containers
- **Azure Container Instances**: Managed containers
- **DigitalOcean App Platform**: Easy deployment

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Future Enhancements

- [ ] User authentication and authorization
- [ ] Real-time updates using WebSockets
- [ ] Payment integration (Stripe, PayPal)
- [ ] Order notifications via email
- [ ] Advanced analytics dashboard
- [ ] Multi-restaurant support
- [ ] Mobile app (React Native)
- [ ] Kubernetes deployment manifests
- [ ] CI/CD pipeline setup
- [ ] Unit and integration tests

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section above
- Review the installation steps

## Acknowledgments

- Built with Flask web framework
- MongoDB for flexible data storage
- Docker for containerization
- Bootstrap for responsive UI
- Twilio for SMS notifications

---

Built with ❤️ using Flask, MongoDB, Docker, and Bootstrap

*A microservices-based food ordering system for customers and employees.*
