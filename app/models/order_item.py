from typing import Any
from pydantic import BaseModel, Field
from app.models.product import Product

# Modelo para registrar un nuevo producto
class OrderItem(BaseModel):
    product: Product
    amount: int