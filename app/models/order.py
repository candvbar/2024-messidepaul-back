from typing import Any, List
from app.models.order_item import OrderItem
from pydantic import BaseModel, Field

# Modelo para registrar un nuevo producto
class Order(BaseModel):
    status: str
    table_number: int
    date: str
    time: str
    total: str
    order_items: List[OrderItem]