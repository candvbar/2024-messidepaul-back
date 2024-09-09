from app.service.product_service import create_product, products, update_product_newprice, update_product_newdescription, delete_product, product_by_id
from app.models.product import Product
from fastapi import HTTPException

def register_new_product(product: Product):
    response = create_product(product.dict())
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "Product registered successfully", "product_id": response["id"]}

def get_products():
    response = products()
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}

def update_product_price(product_id: str, new_price: float):
    response = update_product_newprice(product_id, new_price)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "Product price updated successfully"}

def update_product_description(product_id: str, new_description: str):
    response = update_product_newdescription(product_id, new_description)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "Product description updated successfully"}

def delete(product_id: str):
    response = delete_product(product_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "Product deleted successfully"}

def get_product_by_id(product_id: str):
    response = product_by_id(product_id)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": response}


   