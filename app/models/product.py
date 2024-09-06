from pydantic import BaseModel

# Modelo para registrar un nuevo producto
class Product(BaseModel):
    product_name: str
    product_price: float
    description: str
