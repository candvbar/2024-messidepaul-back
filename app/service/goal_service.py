from calendar import monthrange
from datetime import datetime
from typing import Dict, List
from app.db.firebase import db
from app.models.goal import Goal
from fastapi import HTTPException

def create_goal(goal):
    try:
        # Obtener el siguiente ID disponible
        next_id = get_next_goal_id()

        # Convertir los datos del goal a un formato compatible
        goal_data = goal.dict(by_alias=True, exclude_unset=True)

        if 'actualIncome' not in goal_data:
            goal_data['actualIncome'] = 0

        # Si la fecha ya es una cadena, no se hace nada

        # Handle category_id gracefully (make sure it's None or a valid string)
        if goal_data.get('categoryId') is None:
            goal_data['categoryId'] = None
        elif not isinstance(goal_data.get('categoryId'), str):
            raise Exception("category_id must be a string or None")

        # Guardar el objetivo en Firestore
        new_goal_ref = db.collection('goals').document(str(next_id))
        new_goal_ref.set(goal_data)

        return next_id
    except Exception as e:
        return {"error": str(e)}
        
def get_next_goal_id():
    """
    Obtiene el próximo ID disponible en la colección 'products'.
    """
    try:
        # Obtener todos los documentos de la colección 'products'
        goals = db.collection('goals').stream()

        # Extraer los IDs existentes y convertirlos a enteros
        existing_ids = [int(goal.id) for goal in goals if goal.id.isdigit()]

        if existing_ids:
            # Encontrar el mayor ID existente y sumar 1
            next_id = max(existing_ids) + 1
        else:
            # Si no hay IDs, comenzamos desde 1
            next_id = 1

        return next_id
    except Exception as e:
        raise Exception(f"Error retrieving next ID from existing goals: {str(e)}")

def goals(monthYear):

    # Consultar la colección 'goals' donde el campo 'date' coincide con monthYear
    goals_ref = db.collection('goals').where('date', '==', monthYear)
    docs = goals_ref.stream()

    # Crear una lista de objetivos que cumplen con el filtro
    goals_list = [doc.to_dict() for doc in docs]

    return goals_list