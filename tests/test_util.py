# app/tests/test_utils.py
from app.models import Product

def create_test_product(name='Product Test', price=10.99, description='This is a test product', category=1):
    return Product(name=name, price=price, description=description, category=category)

