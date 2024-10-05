from app.service.product_service import check_product_name_exists, create_product, products, update_product_newprice, update_product_newdescription, delete_product, product_by_id, update_product_newcategories, add_calories
from app.models.product import Product
from app.service.category_service import check_multiple_categories_exist
from fastapi import HTTPException
 # Asegúrate de que esta importación es correcta

def register_new_product(product: Product):

    if check_product_name_exists(product.name):
        raise HTTPException(status_code=400, detail="Product name already exists")

    if(product.name == ""):
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    

    # Validación de precio no numérico y negativo
    try:
        price = float(product.price)  # Intentamos convertir a float
        if price <= 0:
            raise HTTPException(status_code=400, detail="Price cannot be negative or zero")
    except ValueError:
        raise HTTPException(status_code=400, detail="Price must be a number")

    # Verifica si la categoría está en el formato correcto y no está vacía
    category_str = str(product.category).strip()  # Asegúrate de que sea un string y quitar espacios innecesarios
    if not category_str:  # Si la categoría está vacía
        raise HTTPException(status_code=400, detail="Category cannot be empty")

    # Verificar si la categoría existe en Firestore
    category_exists_check = check_multiple_categories_exist(category_str)
    if not category_exists_check:
        raise HTTPException(status_code=400, detail="Category does not exist")

    # Validación de calorías
    if product.calories is None or (isinstance(product.calories, str) and not product.calories.strip()):
        raise HTTPException(status_code=400, detail="Calories cannot be empty or string")

    try:
        # Intentar convertir a float y lanzar excepción si no es válido
        calories = float(product.calories)
        if calories < 0:
            raise HTTPException(status_code=400, detail="Calories must be a positive number")
    except (ValueError, TypeError):  # Captura errores de conversión
        raise HTTPException(status_code=400, detail="Calories must be a valid number")

    # Crea el producto
    product_data = product.dict()
    product_data['category'] = category_str  # Asegúrate de que se guarde como string
    response = create_product(product_data)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])

    return {"message": "Product registered successfully", "id": response["id"]}


def get_products():
    try:
        response = products()  # Llamada a la función que obtiene los productos
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def update_product_price(product_id: str, new_price):
    try:
        # Aseguramos que new_price es un string
        if not isinstance(new_price, str):
            raise HTTPException(status_code=400, detail="Price must be a string")

        # Intentamos convertir a float primero
        new_price_float = float(new_price)

        # Si necesitas una validación adicional para el int, puedes agregarla
        if new_price_float.is_integer():
            new_price = int(new_price_float)
        else:
            new_price = new_price_float

    except ValueError:
        # Si falla la conversión, lanzamos una excepción de validación
        raise HTTPException(status_code=400, detail="Price must be a valid number")

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


def add_food_calories(product_id: str, calories: float):
    try:
        response = add_calories(product_id, calories)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))