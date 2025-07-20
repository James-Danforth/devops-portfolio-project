#!/usr/bin/env python3
"""
Data seeding script for the DevOps portfolio project.
This script populates the database with sample products for demonstration.
"""

from app import create_app, db
from app.models import Product
import os

def seed_products():
    """Seed the database with sample products."""
    app = create_app()
    
    with app.app_context():
        # Create database tables
        db.create_all()
        
        # Sample products data
        products = [
            {
                'name': 'DevOps Handbook',
                'description': 'The definitive guide to DevOps practices and principles',
                'price': 49.99,
                'stock': 25,
                'category': 'Books',
                'image_url': 'https://via.placeholder.com/300x200?text=DevOps+Handbook'
            },
            {
                'name': 'Kubernetes in Action',
                'description': 'Learn Kubernetes from the ground up with practical examples',
                'price': 59.99,
                'stock': 15,
                'category': 'Books',
                'image_url': 'https://via.placeholder.com/300x200?text=Kubernetes+in+Action'
            },
            {
                'name': 'Docker Deep Dive',
                'description': 'Master Docker containers and orchestration',
                'price': 39.99,
                'stock': 30,
                'category': 'Books',
                'image_url': 'https://via.placeholder.com/300x200?text=Docker+Deep+Dive'
            },
            {
                'name': 'Terraform Up & Running',
                'description': 'Infrastructure as Code with Terraform',
                'price': 44.99,
                'stock': 20,
                'category': 'Books',
                'image_url': 'https://via.placeholder.com/300x200?text=Terraform+Up+Running'
            },
            {
                'name': 'Prometheus Monitoring',
                'description': 'Complete guide to monitoring with Prometheus',
                'price': 34.99,
                'stock': 18,
                'category': 'Books',
                'image_url': 'https://via.placeholder.com/300x200?text=Prometheus+Monitoring'
            },
            {
                'name': 'CI/CD Pipeline Guide',
                'description': 'Build robust CI/CD pipelines with GitHub Actions',
                'price': 29.99,
                'stock': 35,
                'category': 'Books',
                'image_url': 'https://via.placeholder.com/300x200?text=CI+CD+Pipeline'
            },
            {
                'name': 'Microservices Architecture',
                'description': 'Design and implement microservices patterns',
                'price': 54.99,
                'stock': 12,
                'category': 'Books',
                'image_url': 'https://via.placeholder.com/300x200?text=Microservices'
            },
            {
                'name': 'Security in DevOps',
                'description': 'DevSecOps practices and security automation',
                'price': 49.99,
                'stock': 22,
                'category': 'Books',
                'image_url': 'https://via.placeholder.com/300x200?text=Security+DevOps'
            }
        ]
        
        # Check if products already exist
        existing_products = Product.query.count()
        if existing_products > 0:
            print(f"Database already contains {existing_products} products. Skipping seed.")
            return
        
        # Add products to database
        for product_data in products:
            product = Product(**product_data)
            db.session.add(product)
        
        # Commit changes
        db.session.commit()
        print(f"Successfully seeded {len(products)} products to the database.")
        
        # Display seeded products
        print("\nSeeded Products:")
        print("=" * 50)
        for product in Product.query.all():
            print(f"• {product.name} - ${product.price} (Stock: {product.stock})")

def main():
    """Main function to run the seeding script."""
    print("Seeding database with sample products...")
    try:
        seed_products()
        print("Database seeding completed successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        return 1
    return 0

if __name__ == '__main__':
    exit(main()) 