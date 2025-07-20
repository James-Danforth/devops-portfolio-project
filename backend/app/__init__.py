from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from prometheus_client import Counter, Histogram
import os

# Initialize extensions
db = SQLAlchemy()

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency')

def create_app(test_config=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
            SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/devops_app'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
        )
    else:
        app.config.update(test_config)

    # Initialize extensions
    db.init_app(app)
    CORS(app)

    # Register blueprints
    from .routes import api
    app.register_blueprint(api, url_prefix='/api')

    # Create database tables
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            # Tables might already exist, which is fine
            print(f"Database initialization note: {e}")

    return app 