from typing import Any
from pydantic import BaseModel, Field
from app.models.product import Product

# Modelo para registrar un nuevo producto
class OrderItem(BaseModel):
    product_id: str
    product_name: str
    product_price: str
    amount: int
