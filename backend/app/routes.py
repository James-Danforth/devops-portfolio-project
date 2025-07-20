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
        user_id = data['user_id']
        product_id = data['product_id']
        quantity = data.get('quantity', 1)
        
        # Check if product exists and has sufficient stock
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        if product.stock < quantity:
            return jsonify({'error': f'Insufficient stock. Available: {product.stock}, Requested: {quantity}'}), 400
        
        # Check if item already exists in cart
        existing_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
        if existing_item:
            # Update quantity if adding more
            new_quantity = existing_item.quantity + quantity
            if product.stock < new_quantity:
                return jsonify({'error': f'Insufficient stock. Available: {product.stock}, Requested: {new_quantity}'}), 400
            existing_item.quantity = new_quantity
            cart_item = existing_item
        else:
            # Create new cart item
            cart_item = Cart(
                user_id=user_id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(cart_item)
        
        db.session.commit()
        
        # Return the cart item data for the test
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

@api.route('/purchase', methods=['POST'])
@track_metrics
def process_purchase():
    """Process a purchase - create order, clear cart, and reduce stock"""
    try:
        data = request.get_json()
        user_id = data['user_id']
        
        # Get user's cart
        cart_items = Cart.query.filter_by(user_id=user_id).all()
        
        if not cart_items:
            return jsonify({'error': 'Cart is empty'}), 400
        
        # Check stock availability and calculate total
        total_amount = 0
        for item in cart_items:
            product = item.product
            if product.stock < item.quantity:
                return jsonify({'error': f'Insufficient stock for {product.name}. Available: {product.stock}, Requested: {item.quantity}'}), 400
            total_amount += product.price * item.quantity
        
        # Create order
        order = Order(
            user_id=user_id,
            total_amount=total_amount,
            status='completed'
        )
        db.session.add(order)
        
        # Reduce stock and clear cart
        for item in cart_items:
            product = item.product
            product.stock -= item.quantity
            db.session.delete(item)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Purchase completed successfully!',
            'order_id': order.id,
            'total_amount': total_amount
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api.route('/reset-market', methods=['POST'])
@track_metrics
def reset_market():
    """Reset the market - clear orders and repopulate products"""
    try:
        # Clear all orders
        Order.query.delete()
        
        # Reset product stock to original values
        products = Product.query.all()
        for product in products:
            # Reset stock based on product ID (original stock values)
            original_stock = {
                1: 25, 2: 15, 3: 30, 4: 20, 5: 18, 6: 35, 7: 12, 8: 22
            }
            product.stock = original_stock.get(product.id, 10)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Market reset successfully! Products have been restocked.',
            'products_count': len(products)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 