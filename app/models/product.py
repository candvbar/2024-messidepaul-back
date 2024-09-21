from typing import Any
from pydantic import BaseModel, Field

# Modelo para registrar un nuevo producto
class Product(BaseModel):
    name: str
    price: Any  # Ensure product_price is non-negative
    description: str
    category: int
