from app.models.product import Product
def get_product_json():
    new_product = {
        "description": "A new product",
        "name": "Product 1",
        "price": 100.00,
        "category": 1,
    }
    return new_product

def get_product():
    new_product = Product(name="Awesome Product", price=9.99, description="This is a great product", category=1)
    return new_product