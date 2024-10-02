from typing import List
from app.db.firebase import db
from app.service.table_service import update_table_status
from app.models.order_item import OrderItem
from fastapi import HTTPException

def create_order(order_data):
    try:
        table_id = str(order_data.get('tableNumber'))
        next_id = get_next_order_id_from_existing()
        # Crear una nueva orden
        orders_ref = db.collection('orders')
        new_order_ref = orders_ref.document(str(next_id))
        new_order_ref.set(order_data)  # Crear la nueva orden en Firebase

        # Cambiar el estado de la mesa a 'BUSY'
        print(table_id)
        if table_id:
            update_table_status(table_id, "BUSY")

        return {
            "message": "Order created successfully",
            "order_id": next_id,  # Devuelve el ID de la nueva orden
            "order": order_data  # También puedes devolver los datos de la orden
        }
    except Exception as e:
        return {"error": str(e)}

def finalize_order(order_id: str):
    """
    Finaliza una orden y, si no hay más órdenes activas en la mesa, cambia el estado de la mesa a "free".
    """
    try:
        # Obtener la orden por su ID
        order_ref = db.collection('orders').document(order_id)
        order = order_ref.get()

        if not order.exists:
            raise HTTPException(status_code=404, detail="Order not found")

        order_data = order.to_dict()
        table_id = str(order_data.get('tableNumber'))

        # Actualizar el estado de la orden como finalizada
        order_ref.update({"status": "finalized"})

        # Verificar si hay más órdenes activas en la mesa
        if table_id:
            active_orders = db.collection('orders').where('table_id', '==', table_id).where('status', '!=', 'finalized').stream()
            active_order_list = list(active_orders)

            # Si no hay más órdenes activas, liberar la mesa
            if not active_order_list:
                update_table_status(table_id, "FREE")

        return {"message": "Order finalized successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_order_by_id(order_id: str):
    """
    Obtiene una orden por su ID.
    """
    try:
        order_ref = db.collection('orders').document(order_id)
        order_doc = order_ref.get()
        print(order_doc.to_dict())
        if not order_doc.exists:
            return None
        return order_doc.to_dict()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving order: {str(e)}")


def get_all_orders():
    """
    Obtiene todas las órdenes de la colección 'orders'.
    """
    try:
        orders_ref = db.collection('orders').stream()
        orders_list = []

        for order in orders_ref:
            order_data = order.to_dict()
            order_data['id'] = order.id
            orders_list.append(order_data)

        return orders_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving orders: {str(e)}")

def get_next_order_id_from_existing():
    """
    Obtiene el próximo ID disponible en la colección 'products'.
    """
    try:
        # Obtener todos los documentos de la colección 'products'
        orders = db.collection('orders').stream()

        # Extraer los IDs existentes y convertirlos a enteros
        existing_ids = [int(order.id) for order in orders if order.id.isdigit()]

        if existing_ids:
            # Encontrar el mayor ID existente y sumar 1
            next_id = max(existing_ids) + 1
        else:
            # Si no hay IDs, comenzamos desde 1
            next_id = 1

        return next_id
    except Exception as e:
        raise Exception(f"Error retrieving next ID from existing products: {str(e)}")

def update_order(order_id: str, updated_order_data: dict):
    try:
        # Reference to the order in the database
        order_ref = db.collection('orders').document(order_id)
        
        # Perform the update in the database
        order_ref.update(updated_order_data)
        return {"message": "Order updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def add_items_to_order(order_id: str, new_items: List[OrderItem], total: str):
    existing_order = get_order_by_id(order_id)
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Preparar los datos de la orden actualizados con los nuevos ítems (viejos y nuevos ya incluidos en 'new_items')
    order_copy = existing_order.copy()
    order_copy["orderItems"] = [item.dict() for item in new_items]  # Reemplazar directamente los ítems
    order_copy["total"] = total  # Actualizar el total
    
    # Actualizar la orden en la base de datos
    response = update_order(order_id, order_copy)

    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    
    return response
