from typing import Any, List
from app.models.order_item import OrderItem
from pydantic import BaseModel, Field

# Modelo para registrar un nuevo producto
class Order(BaseModel):
    status: str
    amountOfPeople: int
    tableNumber: int
    date: str
    time: str
    total: str
    orderItems: List[OrderItem]