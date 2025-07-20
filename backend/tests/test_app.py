import pytest
from app import create_app, db
from app.models import Product, Cart, Order

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'test-secret-key'
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

def test_health_check(client):
    """Test health check endpoint."""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'backend-api'

def test_get_products_empty(client):
    """Test getting products when none exist."""
    response = client.get('/api/products')
    assert response.status_code == 200
    data = response.get_json()
    assert data == []

def test_create_product(client):
    """Test creating a new product."""
    product_data = {
        'name': 'Test Product',
        'description': 'A test product',
        'price': 29.99,
        'stock': 10,
        'category': 'Electronics',
        'image_url': 'https://example.com/image.jpg'
    }
    
    response = client.post('/api/products', json=product_data)
    assert response.status_code == 201
    
    data = response.get_json()
    assert data['name'] == product_data['name']
    assert data['price'] == product_data['price']
    assert data['stock'] == product_data['stock']

def test_get_product(client):
    """Test getting a specific product."""
    # First create a product
    product_data = {
        'name': 'Test Product',
        'description': 'A test product',
        'price': 29.99,
        'stock': 10
    }
    
    create_response = client.post('/api/products', json=product_data)
    created_product = create_response.get_json()
    
    # Then get the product
    response = client.get(f'/api/products/{created_product["id"]}')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['name'] == product_data['name']
    assert data['price'] == product_data['price']

def test_add_to_cart(client):
    """Test adding item to cart."""
    # First create a product
    product_data = {
        'name': 'Test Product',
        'description': 'A test product',
        'price': 29.99,
        'stock': 10
    }
    
    create_response = client.post('/api/products', json=product_data)
    created_product = create_response.get_json()
    
    # Add to cart
    cart_data = {
        'user_id': 'user123',
        'product_id': created_product['id'],
        'quantity': 2
    }
    
    response = client.post('/api/cart', json=cart_data)
    assert response.status_code == 201
    
    data = response.get_json()
    assert data['user_id'] == cart_data['user_id']
    assert data['product_id'] == cart_data['product_id']
    assert data['quantity'] == cart_data['quantity']

def test_get_cart(client):
    """Test getting user's cart."""
    # First create a product and add to cart
    product_data = {
        'name': 'Test Product',
        'description': 'A test product',
        'price': 29.99,
        'stock': 10
    }
    
    create_response = client.post('/api/products', json=product_data)
    created_product = create_response.get_json()
    
    cart_data = {
        'user_id': 'user123',
        'product_id': created_product['id'],
        'quantity': 1
    }
    
    client.post('/api/cart', json=cart_data)
    
    # Get cart
    response = client.get('/api/cart/user123')
    assert response.status_code == 200
    
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['user_id'] == 'user123'

def test_create_order(client):
    """Test creating a new order."""
    order_data = {
        'user_id': 'user123',
        'total_amount': 59.98,
        'status': 'pending'
    }
    
    response = client.post('/api/orders', json=order_data)
    assert response.status_code == 201
    
    data = response.get_json()
    assert data['user_id'] == order_data['user_id']
    assert data['total_amount'] == order_data['total_amount']
    assert data['status'] == order_data['status']

def test_get_orders(client):
    """Test getting all orders."""
    # First create an order
    order_data = {
        'user_id': 'user123',
        'total_amount': 59.98,
        'status': 'pending'
    }
    
    client.post('/api/orders', json=order_data)
    
    # Get all orders
    response = client.get('/api/orders')
    assert response.status_code == 200
    
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['user_id'] == order_data['user_id'] 