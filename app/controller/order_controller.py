from app.service.order_service import create_order, finalize_order, get_order_by_id, get_all_orders
from app.models.order import Order
from fastapi import HTTPException
from app.service.product_service import product_by_id

def register_new_order(order: Order):
    order_data = order.dict()
    
    # Validar que la mesa esté incluida en la orden
    table_id = order_data.get('table_number')
    if not table_id:
        raise HTTPException(status_code=400, detail="Table ID is required")
    
    print(order_data)

    # Obtener datos de los productos desde la orden
    order_items = order_data.get('order_items', [])
    if not order_items:
        raise HTTPException(status_code=400, detail="At least one order item is required")

    for item in order_items:
        product_id = item.get('product', {}).get('id')
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

    return {"message": "Order registered successfully", "order_id": response["order_id"]}
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
