from app.service.table_service import associate_order_with_table, get_tables_service, get_table_by_id, update_table_status
from app.models.table import Table
from fastapi import HTTPException
from app.service.order_service import get_order_by_id


def get_tables_controller():
    """
    Controlador para obtener todas las categorías.
    """
    return get_tables_service()

def get_table_by_id_controller(table_id: str):
    """
    Controlador para obtener una categoría por ID.
    """
    table = get_table_by_id(table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return table

def update_table_status_controller(table_id: str, new_status: str):
    try:
        response = update_table_status(table_id, new_status)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_order_for_table(table_id: str):
    # Fetch the table
    table = await get_table_by_id(table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")

    # Check if there is an associated order
    order = await get_order_by_id(table.order_id)  # Adjust this function based on your order retrieval logic
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Check if the order status is 'in progress'
    if order.status != 'in progress':
        raise HTTPException(status_code=400, detail="Order is not in progress")

    return order

def associate_order_with_table_controller(table_id: str, order_id: str):
    print(table_id)
    print(order_id)
    response = associate_order_with_table(table_id, order_id)
    if 'error' in response:
        raise HTTPException(status_code=400, detail=response['error'])
    return response
