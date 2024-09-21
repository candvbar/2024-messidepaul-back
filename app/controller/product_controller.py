from app.service.product_service import create_product, products, update_product_newprice, update_product_newdescription, delete_product, product_by_id
from app.models.product import Product
from fastapi import HTTPException
 # Asegúrate de que esta importación es correcta

def register_new_product(product: Product):
    # Validación de precio no numérico y negativo
    if isinstance(product.price, (int, float)):
        if product.price < 0:
            raise HTTPException(status_code=400, detail="Price cannot be negative")
    else:
        raise HTTPException(status_code=400, detail="Price must be a number")
    
    response = create_product(product.dict())
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    
    return {"message": "Product registered successfully", "id": response["id"]}

def get_products():
    try:
        response = products()  # Llamada a la función que obtiene los productos
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def update_product_price(product_id: str, new_price: float):
    try:
        response = update_product_newprice(product_id, new_price)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def update_product_description(product_id: str, new_description: str):
    try:
        response = update_product_newdescription(product_id, new_description)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def delete_product_by_id(product_id: str):
    try:
        response = delete_product(product_id)
        return None  # No retorno en caso de éxito
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_product_by_id(product_id: str):
    try:
        response = product_by_id(product_id)
        if "error" in response:
            raise HTTPException(status_code=404, detail=response["error"])  # Lanzar 404 si el producto no se encuentra
        
        return response  # Si no hay error, devolver la respuesta normal

    except HTTPException as http_exception:
        raise http_exception  # Propagar excepciones HTTP
    except Exception as e:
        # Lanzar 500 para otros errores
        raise HTTPException(status_code=500, detail=str(e))





   