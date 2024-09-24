from typing import Any
from pydantic import BaseModel, Field

# Modelo para registrar un nuevo producto
class Table(BaseModel):
    status: str
    table_id: int