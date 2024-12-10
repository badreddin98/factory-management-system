# Factory Management System

This is a Flask-based Factory Management System that implements pagination and advanced querying capabilities using SQLAlchemy.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

## API Endpoints

### Pagination Endpoints

1. Get Orders (Paginated)
```
GET /orders?page=1&per_page=10
```

2. Get Products (Paginated)
```
GET /products?page=1&per_page=10
```

### Advanced Query Endpoints

1. Employee Performance Analysis
```
GET /employee-performance
```

2. Top Selling Products
```
GET /top-selling-products
```

3. Customer Lifetime Value
```
GET /customer-lifetime-value?threshold=1000
```

4. Production Efficiency
```
GET /production-efficiency?date=2024-12-10
```

## Database Schema

The system uses the following models:
- Employee
- Product
- Customer
- Order
- OrderItem
- Production

Each model contains relevant fields and relationships to support the system's functionality.

## Features

1. **Pagination Implementation**
   - Support for page and per_page parameters
   - Efficient retrieval of data in smaller chunks
   - Proper handling of edge cases

2. **Advanced Querying**
   - Employee performance tracking
   - Product sales analysis
   - Customer value assessment
   - Production efficiency monitoring

## Error Handling

The system includes proper error handling for:
- Invalid page numbers
- Out-of-range requests
- Invalid date formats
- Missing parameters
