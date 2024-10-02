from typing import List
from app.service.order_service import create_order, finalize_order, get_order_by_id, get_all_orders, add_items_to_order
from app.models.order import Order
from app.models.order import OrderItem
from fastapi import HTTPException
from app.service.product_service import product_by_id
from app.service.table_service import get_table_by_id

def register_new_order(order: Order):
    order_data = order.dict()

    # Validar que la mesa esté incluida en la orden
    table_id = order_data.get('tableNumber')
    if not table_id:
        raise HTTPException(status_code=400, detail="Table ID is required")

    # Verificar si la mesa existe utilizando get_table_by_id directamente
    table = get_table_by_id(str(table_id))  # Asegúrate de que sea string si es necesario
    if not table:
        raise HTTPException(status_code=404, detail=f"Table with ID {table_id} not found")

    print(order_data)

    # Obtener datos de los productos desde la orden
    order_items = order_data.get('orderItems', [])
    if not order_items:
        raise HTTPException(status_code=400, detail="At least one order item is required")

    for item in order_items:
        # Obtener product_id del item
        product_id = item.get('product_id')
        if not product_id:
            raise HTTPException(status_code=400, detail="Product ID is required in the order item")
        
        # Verificar si el producto existe en la base de datos
        product = product_by_id(product_id)
        if "error" in product:
            raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")

        # Validar que la cantidad de producto sea mayor que 0
        amount = item.get('amount')
        if not amount or amount <= 0:
            raise HTTPException(status_code=400, detail="Product amount must be greater than zero")

    # Validaciones completas, proceder a crear la orden
    response = create_order(order_data)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])

    return response

def finalize_order_controller(order_id: str):
    try:
        response = finalize_order(order_id)
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_order_controller(order_id: str):
    try:
        response = get_order_by_id(order_id)
        if not response:
            raise HTTPException(status_code=404, detail="Order not found")
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_orders():
    try:
        response = get_all_orders()
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def add_order_items(order_id: str, new_order_items: List[OrderItem], total: str):
    try:
        # Fetch the existing order
        existing_order = get_order_by_id(order_id)
        if not existing_order:
            raise HTTPException(status_code=404, detail="Order not found")

        # Check if the order status is 'in progress'
        if existing_order.get("status") != "in progress":
            raise HTTPException(status_code=400, detail="Cannot add items to an order that is not in progress")

        # Validate that each product_id exists in the products table
        for item in new_order_items:
            product_id = item.product_id
            product = product_by_id(product_id)  # Fetch product details by product_id
            if "error" in product:
                raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")

        
        response = add_items_to_order(order_id, new_order_items)
        return response
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

