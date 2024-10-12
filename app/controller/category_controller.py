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
        orders = get_orders_by_status('FINALIZED')
        category_revenue = {}

        for order in orders:
            for item in order['orderItems']:
                product_id = item['product_id']
                amount = item['amount']

                product = product_by_id(product_id)

                if 'product' in product:
                    # Extract the category ID from the product
                    category = product['product'].get('category')

                    category_name = None
                    
                    # Check if category is a string (category ID)
                    if isinstance(category, str):
                        category_data = get_category_by_id_controller(category.strip())  # Fetch category by ID
                        category_name = category_data.get('name') if category_data else None
                    elif isinstance(category, dict):
                        category_name = category.get('name')  # If category is a dict

                    # Check if we have a valid category name
                    if category_name:
                        if category_name not in category_revenue:
                            category_revenue[category_name] = 0
                        price = float(product['product']['price'])
                        cost = float(product['product']['cost'])
                        category_revenue[category_name] += (price - cost) * amount
                    else:
                        print(f"Product with ID {product_id} does not have a valid category name.")

        return category_revenue

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating category revenue: {str(e)}")

