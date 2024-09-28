from app.service.product_service import create_product, products, update_product_newprice, update_product_newdescription, delete_product, product_by_id, update_product_newcategories
from app.models.product import Product
from app.service.category_service import check_multiple_categories_exist
from fastapi import HTTPException
 # Asegúrate de que esta importación es correcta

def register_new_product(product: Product):
    # Validación de precio no numérico y negativo
    price = float(product.price)
    if isinstance(price, (int, float)):
        if price <= 0:
            raise HTTPException(status_code=400, detail="Price cannot be negative or zero")
    else:
        raise HTTPException(status_code=400, detail="Price must be a number")

    # Verificar si la categoría existe en Firestore
    category_exists_check = check_multiple_categories_exist(product.category)
    if not category_exists_check:
        raise HTTPException(status_code=400, detail="Category does not exist")

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
    
def update_product_categories(product_id: str, newcategories: str):
    try:
        response = update_product_newcategories(product_id, newcategories)
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
            raise HTTPException(status_code=404, detail=response["error"])

        return response

    except HTTPException as http_exception:
        raise http_exception 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





   