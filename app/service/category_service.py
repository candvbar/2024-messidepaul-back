from app.db.firebase import db
from app.models.category import Category
from fastapi import HTTPException

def get_next_id_from_existing():
    """
    Obtiene el próximo ID disponible en la colección 'category'.
    """
    try:
        # Obtener todos los documentos de la colección 'category'
        categories = db.collection('category').stream()
        
        # Extraer los IDs existentes y convertirlos a enteros
        existing_ids = [int(category.id) for category in categories if category.id.isdigit()]

        if existing_ids:
            # Encontrar el mayor ID existente y sumar 1
            next_id = max(existing_ids) + 1
        else:
            # Si no hay IDs, comenzamos desde 1
            next_id = 1

        return next_id
    except Exception as e:
        raise Exception(f"Error retrieving next ID from existing categories: {str(e)}")


def create_category(category_data):
    """
    Crea una nueva categoría asegurando que el ID no colisione con uno existente.
    """
    try:
        # Obtén el siguiente ID disponible
        next_id = get_next_id_from_existing()
        # Crea el nuevo documento con el ID autoincremental
        new_category_ref = db.collection('category').document(str(next_id))
        new_category_ref.set(category_data)

        return {"message": "Category added successfully", "id": next_id}
    except Exception as e:
        return {"error": str(e)}

def register_new_category(category: Category):
    if category.type == "Default":
        raise HTTPException(status_code=400, detail="Cannot create a category with type 'Default'")
    
    response = create_category(category.dict())
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    
    return {"message": "Category registered successfully", "id": response["id"]}

def update_category_name(category_id: str, new_name: str):
    try:
        category_ref = db.collection('category').document(category_id)
        category = category_ref.get()
        
        if not category.exists:
            raise HTTPException(status_code=404, detail="Category not found")
        
        category_data = category.to_dict()
        
        if category_data['type'] == "Default":
            raise HTTPException(status_code=400, detail="Cannot edit the name of a 'Default' category")
        
        # Actualizar solo el nombre de la categoría
        category_ref.update({"name": new_name})
        
        return {"message": "Category name updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_categories():
    """
    Servicio para obtener todas las categorías desde Firebase.
    """
    try:
        categories_ref = db.collection('category').stream()
        categories = []
        for category in categories_ref:
            cat = category.to_dict()
            cat['id'] = category.id  # Añadir el ID a la respuesta
            categories.append(cat)
        return {"categories": categories}
    except Exception as e:
        return {"error": str(e)}

def get_category_by_id(category_id: str):
    """
    Servicio para obtener una categoría por su ID.
    """
    try:
        category_ref = db.collection('category').document(category_id).get()
        if category_ref.exists:
            category = category_ref.to_dict()
            category['id'] = category_ref.id
            return category
        else:
            return None  # Si la categoría no existe
    except Exception as e:
        return {"error": str(e)}

def delete_category_by_id(category_id: str):
    """
    Servicio para eliminar una categoría por su ID.
    """
    try:
        category_ref = db.collection('category').document(category_id)
        if category_ref.get().exists:
            category_ref.delete()
            return {"message": "Category deleted successfully"}
        else:
            return {"error": "Category not found"}
    except Exception as e:
        return {"error": str(e)}

def update_category_name(category_id: str, new_name: str):
    """
    Servicio para actualizar el nombre de una categoría.
    """
    try:
        category_ref = db.collection('category').document(category_id)
        if category_ref.get().exists:
            category_ref.update({"name": new_name})
            return {"message": "Category name updated successfully"}
        else:
            return {"error": "Category not found"}
    except Exception as e:
        return {"error": str(e)}

def category_exists(category_id: int) -> bool:
    """
    Verifica si una categoría con el ID proporcionado existe en Firestore.
    """
    try:
        # Aquí suponemos que category_id es un número, así que lo usamos directamente
        category_ref = db.collection('category').document(str(category_id))  # Si Firestore requiere un string, mantén esto
        return category_ref.get().exists  # Devuelve True si existe, False si no
    except Exception as e:
        raise Exception(f"Error al verificar la categoría con ID {category_id}: {str(e)}")

def check_multiple_categories_exist(category_str: str) -> bool:
    try:
        # Convertimos los IDs de string a entero
        category_ids = [int(category_id.strip()) for category_id in category_str.split(",") if category_id.strip()]
        print(category_ids)
        for category_id in category_ids:
            exists = category_exists(category_id)
            if not exists:
                raise Exception(f"Category with id {category_id} does not exist.")
        return True
    except ValueError as e:
        raise Exception(f"Error al verificar múltiples categorías: {str(e)}")


'''def get_default_categories_service():
    """
    Servicio para obtener todas las categorías de tipo 'Default' desde Firebase.
    """
    try:
        categories_ref = db.collection('category').where('type', '==', 'Default').stream()
        default_categories = []
        for category in categories_ref:
            cat = category.to_dict()
            cat['id'] = category.id  # Añadir el ID a la respuesta
            default_categories.append(cat)
        return default_categories
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving default categories: {str(e)}")'''
