from app.service.category_service import create_category, get_categories, get_category_by_id, delete_category_by_id, update_category_name
from app.models.category import Category
from fastapi import HTTPException

def register_new_category(category: Category):
    """
    Controlador que valida y registra una nueva categoría.
    """
    # Validar si el tipo es una cadena
    if not isinstance(category.type, str):
        raise HTTPException(status_code=400, detail="Category type must be a string")
    
    # Impedir que se registren categorías de tipo Default
    if category.type == "Default":
        raise HTTPException(status_code=400, detail="Category type cannot be 'Default'")
    if category.type != "Custom":
        category.type = "Custom"
    # Llamar al servicio para crear la categoría
    response = create_category(category.dict())
    
    # Si hay un error, lanzar una excepción HTTP
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    
    # Si todo va bien, devolver la respuesta
    return {"message": "Category registered successfully", "id": response["id"]}

def get_all_categories():
    """
    Controlador para obtener todas las categorías.
    """
    return get_categories()

def get_category_by_id_controller(category_id: str):
    """
    Controlador para obtener una categoría por ID.
    """
    category = get_category_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

def delete_category_controller(category_id: str):
    """
    Controlador para eliminar una categoría.
    """
    category = get_category_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    if category['type'] == "Default":
        raise HTTPException(status_code=400, detail="Cannot delete a 'Default' category")

    return delete_category_by_id(category_id)

def update_category_name_controller(category_id: str, new_name: str):
    """
    Controlador para actualizar el nombre de una categoría.
    """
    category = get_category_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    if category['type'] == "Default":
        raise HTTPException(status_code=400, detail="Cannot edit the name of a 'Default' category")

    return update_category_name(category_id, new_name)
