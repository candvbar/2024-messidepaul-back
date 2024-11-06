from calendar import monthrange
from datetime import datetime
from typing import Dict, List
from app.db.firebase import db
from app.models.goal import Goal
from fastapi import HTTPException
from collections import defaultdict
from datetime import datetime, timedelta
from google.cloud import firestore
from app.service.category_service import get_categories
from app.service.product_service import products

def create_goal(goal):
    try:
        # Obtener el siguiente ID disponible
        next_id = get_next_goal_id()

        # Convertir los datos del goal a un formato compatible
        goal_data = goal.dict(by_alias=True, exclude_unset=True)

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


def get_category_product_mapping():
    try:
        # Fetch products
        products_response = products()  # Assuming this fetches the products from Firestore
        products_list = products_response.get("products", [])

        # Create a dictionary to hold category IDs as keys and a set of product IDs as values
        category_to_products = defaultdict(set)

        # Iterate through each product to associate it with categories
        for product in products_list:
            product_id = product.get('id')  # The product ID is stored under 'id'
            category_ids = product.get('category', '').split(',')  # Split categories string by comma
            
            for category_id in category_ids:
                category_id = category_id.strip()  # Remove any leading/trailing whitespace
                category_to_products[category_id].add(product_id)

        # Convert sets to comma-separated strings
        category_to_products = {category_id: ','.join(sorted(product_ids)) for category_id, product_ids in category_to_products.items()}
        print("HOLAAAAAA", category_to_products)
        return category_to_products

    except Exception as e:
        return {"error": str(e)}


def goals(monthYear):
    try:
        # Parsear monthYear en fechas de inicio y fin
        start_date = datetime.strptime(monthYear, "%m/%y")
        end_date = start_date.replace(day=28) + timedelta(days=4)  # Mover al próximo mes
        end_date = end_date - timedelta(days=end_date.day)  # Ajustar al último día del mes

        # Consultar la colección 'goals' para el mes y año especificados
        goals_ref = db.collection('goals').where('date', '==', monthYear).stream()
        goals = []
        category_products = get_category_product_mapping()  # Mapear categorías a productos

        for goal in goals_ref:
            gol = goal.to_dict()
            gol['id'] = goal.id  # Incluir el ID del goal
            
            # Inicializar el seguimiento del ingreso
            actual_income = 0
            category_id = gol.get('categoryId')

            # Consultar pedidos finalizados dentro del rango de fechas
            orders_ref = db.collection('orders')
            orders_ref = orders_ref \
                .where("status", "==", "FINALIZED") \
                .where("date", ">=", start_date.strftime("%Y-%m-%d")) \
                .where("date", "<=", end_date.strftime("%Y-%m-%d")) \
                .stream()

            if category_id is None:
                # Sumar todos los totales de pedidos cuando no hay filtro de categoría
                for order in orders_ref:
                    order_data = order.to_dict()
                    actual_income += float(order_data.get('total', 0))
            else:
                # Filtrar ingresos basado en la categoría-producto
                for order in orders_ref:
                    order_data = order.to_dict()
                    for item in order_data.get('orderItems', []):
                        product_id = item.get('product_id')
                        if product_id:
                            # Verificar si el producto pertenece a la categoría de la meta
                            associated_categories = category_products.get(str(category_id), "").split(',')
                            if str(product_id) in associated_categories:
                                # Calcular ingresos multiplicando cantidad y precio
                                product_price = item.get('product_price', 0)
                                amount = item.get('amount', 0)
                                actual_income += amount * float(product_price)

            gol['actualIncome'] = actual_income  # Actualizar la meta con el ingreso real
            db.collection('goals').document(goal.id).update({
                'actualIncome': actual_income
            })
            goals.append(gol)

        return goals

    except Exception as e:
        return {"error": str(e)}