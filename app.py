from flask import Flask, jsonify, request
from models import db, Employee, Product, Customer, Order, OrderItem, Production
from sqlalchemy import func
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///factory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# Pagination endpoints
@app.route('/orders')
def get_orders():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    orders = Order.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'orders': [{
            'id': order.id,
            'customer_id': order.customer_id,
            'order_date': order.order_date.isoformat(),
            'items': [{
                'product_id': item.product_id,
                'quantity': item.quantity
            } for item in order.items]
        } for order in orders.items],
        'total_pages': orders.pages,
        'current_page': orders.page,
        'total_items': orders.total
    })

@app.route('/products')
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    products = Product.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'products': [{
            'id': product.id,
            'name': product.name,
            'price': product.price
        } for product in products.items],
        'total_pages': products.pages,
        'current_page': products.page,
        'total_items': products.total
    })

# Advanced query endpoints
@app.route('/employee-performance')
def employee_performance():
    performance = db.session.query(
        Employee.name,
        func.sum(Production.quantity).label('total_produced')
    ).join(Production).group_by(Employee.name).all()
    
    return jsonify([{
        'employee_name': name,
        'total_produced': total
    } for name, total in performance])

@app.route('/top-selling-products')
def top_selling_products():
    top_products = db.session.query(
        Product.name,
        func.sum(OrderItem.quantity).label('total_ordered')
    ).join(OrderItem).group_by(Product.name)\
    .order_by(func.sum(OrderItem.quantity).desc()).all()
    
    return jsonify([{
        'product_name': name,
        'total_ordered': total
    } for name, total in top_products])

@app.route('/customer-lifetime-value')
def customer_lifetime_value():
    threshold = request.args.get('threshold', 1000, type=float)
    
    customer_value = db.session.query(
        Customer.name,
        func.sum(Product.price * OrderItem.quantity).label('total_value')
    ).join(Order).join(OrderItem).join(Product)\
    .group_by(Customer.name)\
    .having(func.sum(Product.price * OrderItem.quantity) >= threshold)\
    .all()
    
    return jsonify([{
        'customer_name': name,
        'total_value': float(value)
    } for name, value in customer_value])

@app.route('/production-efficiency')
def production_efficiency():
    date_str = request.args.get('date', datetime.utcnow().date().isoformat())
    date = datetime.fromisoformat(date_str)
    
    efficiency = db.session.query(
        Product.name,
        func.sum(Production.quantity).label('total_produced')
    ).join(Production)\
    .filter(func.date(Production.production_date) == date.date())\
    .group_by(Product.name).all()
    
    return jsonify([{
        'product_name': name,
        'total_produced': total
    } for name, total in efficiency])

if __name__ == '__main__':
    app.run(debug=True)
