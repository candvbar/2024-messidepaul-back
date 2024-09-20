from pydantic import BaseModel, Field

# Modelo para registrar un nuevo producto
class Category(BaseModel):
    name: str
    type: str