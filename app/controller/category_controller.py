from app.service.category_service import check_category_name_exists, create_category, get_categories, get_category_by_id, delete_category_by_id, update_category_name
from app.models.category import Category
from fastapi import HTTPException
from app.service.order_service import get_orders_by_status
from app.service.product_service import product_by_id

def register_new_category(category: Category):
    """
    Controlador que valida y registra una nueva categoría.
    """
    if not isinstance(category.type, str):
        raise HTTPException(status_code=400, detail="Category type must be a string")
    
    if category.type == "Default":
        raise HTTPException(status_code=400, detail="Category type cannot be 'Default'")
    if category.type != "Custom":
        category.type = "Custom"
    
    if check_category_name_exists(category.name):
        raise HTTPException(status_code=400, detail="Category name already exists")

    response = create_category(category.dict())
    
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    
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

def get_category_revenue_controller():
    try:
        orders = get_orders_by_status('FINALIZED')  # Retrieve finalized orders
        category_revenue = {}

        # Loop through all orders and collect product information
        for order in orders:
            for item in order['orderItems']:
                product_id = item['product_id']
                amount = item['amount']

                # Retrieve product details by product_id
                product = product_by_id(product_id)  # Assumes you have a function to fetch product by ID

                # Check if 'category' exists in the product data
                if 'product' in product and 'category' in product['product']:
                    categories = product['product']['category'].split(',')

                    for category in categories:
                        category = category.strip()
                        if category not in category_revenue:
                            category_revenue[category] = 0

                        # Use the price from the product dictionary
                        price = float(product['product']['price'])  # Make sure to convert price to float if necessary
                        cost = float(product['product']['cost'])  # Make sure to convert cost to float if necessary
                        category_revenue[category] += (price - cost) * amount
                else:
                    print(f"Product with ID {product_id} does not have a category.")

        return category_revenue

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating category revenue: {str(e)}")