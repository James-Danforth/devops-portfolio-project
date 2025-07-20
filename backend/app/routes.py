from flask import Blueprint, request, jsonify
from . import db, REQUEST_COUNT, REQUEST_LATENCY
from .models import Product, Cart, Order
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import time

api = Blueprint('api', __name__)

def track_metrics(func):
    """Decorator to track Prometheus metrics"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            response = func(*args, **kwargs)
            # Handle tuple responses (response, status_code)
            if isinstance(response, tuple):
                status_code = response[1] if len(response) > 1 else 200
            else:
                status_code = response.status_code if hasattr(response, 'status_code') else 200
            REQUEST_COUNT.labels(method=request.method, endpoint=request.endpoint, status=status_code).inc()
            return response
        except Exception as e:
            REQUEST_COUNT.labels(method=request.method, endpoint=request.endpoint, status=500).inc()
            raise e
        finally:
            REQUEST_LATENCY.observe(time.time() - start_time)
    wrapper.__name__ = func.__name__
    return wrapper

@api.route('/health')
@track_metrics
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'backend-api'})

@api.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

# Product endpoints
@api.route('/products', methods=['GET'])
@track_metrics
def get_products():
    """Get all products"""
    try:
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/products/<int:product_id>', methods=['GET'])
@track_metrics
def get_product(product_id):
    """Get a specific product"""
    try:
        product = Product.query.get_or_404(product_id)
        return jsonify(product.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/products', methods=['POST'])
@track_metrics
def create_product():
    """Create a new product"""
    try:
        data = request.get_json()
        product = Product(
            name=data['name'],
            description=data.get('description', ''),
            price=data['price'],
            stock=data.get('stock', 0),
            category=data.get('category', ''),
            image_url=data.get('image_url', '')
        )
        db.session.add(product)
        db.session.commit()
        return jsonify(product.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Cart endpoints
@api.route('/cart/<user_id>', methods=['GET'])
@track_metrics
def get_cart(user_id):
    """Get user's cart"""
    try:
        cart_items = Cart.query.filter_by(user_id=user_id).all()
        return jsonify([item.to_dict() for item in cart_items]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/cart', methods=['POST'])
@track_metrics
def add_to_cart():
    """Add item to cart"""
    try:
        data = request.get_json()
        cart_item = Cart(
            user_id=data['user_id'],
            product_id=data['product_id'],
            quantity=data.get('quantity', 1)
        )
        db.session.add(cart_item)
        db.session.commit()
        return jsonify(cart_item.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api.route('/cart/<int:cart_id>', methods=['DELETE'])
@track_metrics
def remove_from_cart(cart_id):
    """Remove item from cart"""
    try:
        cart_item = Cart.query.get_or_404(cart_id)
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'message': 'Item removed from cart'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Order endpoints
@api.route('/orders', methods=['GET'])
@track_metrics
def get_orders():
    """Get all orders"""
    try:
        orders = Order.query.all()
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/orders/<user_id>', methods=['GET'])
@track_metrics
def get_user_orders(user_id):
    """Get user's orders"""
    try:
        orders = Order.query.filter_by(user_id=user_id).all()
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/orders', methods=['POST'])
@track_metrics
def create_order():
    """Create a new order"""
    try:
        data = request.get_json()
        order = Order(
            user_id=data['user_id'],
            total_amount=data['total_amount'],
            status=data.get('status', 'pending')
        )
        db.session.add(order)
        db.session.commit()
        return jsonify(order.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 