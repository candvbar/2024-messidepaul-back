from pydantic import BaseModel, validator, Field

# Modelo para registrar un nuevo producto
class Product(BaseModel):
    product_name: str
    product_price: float = Field(..., ge=0)  # Ensure product_price is non-negative
    description: str

    @validator('product_price')
    def check_product_price(cls, v):
        if v < 0:
            raise ValueError('Product price must be non-negative')
        return v