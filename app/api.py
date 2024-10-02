from typing import Any, Dict, List
from fastapi import APIRouter
from app.models.user import UserLogin, UserRegister, UserForgotPassword, TokenData
from app.models.product import Product
from app.models.category import Category
from app.models.order import Order
from app.controller.user_controller import login, register, handle_forgot_password, get_user_by_id, delete_user_by_id, token
from app.controller.product_controller import register_new_product, get_products, update_product_price, update_product_description, delete_product_by_id, get_product_by_id, update_product_categories, add_food_calories
from app.controller.category_controller import delete_category_controller, get_all_categories, get_category_by_id_controller, register_new_category, update_category_name_controller
from app.controller.table_controller import associate_order_with_table_controller, get_table_by_id_controller, get_tables_controller, update_table_status_controller
from app.controller.order_controller import register_new_order, finalize_order_controller, get_orders, get_order_controller, add_order_items
from app.models.order_item import OrderItem

router = APIRouter()

@router.get("/")
async def root():
    return "Server is running"

# Ruta para iniciar sesión
@router.post("/login/")
async def login_user(user: UserLogin):
    return login(user)


@router.post("/verify-token/")
async def verify_token(token_data: TokenData):
    return token(token_data)

#------------------------USER--------------------------
# Ruta para registrar un nuevo usuario
@router.post("/register/")
async def register_user(user: UserRegister):
    return register(user)

# Ruta para recuperación de contraseña
@router.post("/forgot-password/")
async def forgot_password_user(user: UserForgotPassword):
    return handle_forgot_password(user)

@router.get("/users/{uid}")
async def get_user(uid: str):
    return get_user_by_id(uid)

@router.delete("/users/{uid}")
async def delete_user(uid: str):
    return delete_user_by_id(uid)

#------------------------PRODUCTO--------------------------

#validaciones
@router.post("/register-product")
async def register_product(product: Product):
    print(product)
    return register_new_product(product) 

@router.get("/products")
async def products():
    return get_products()

@router.put("/products/price/{product_id}/{new_price}")
async def update_price(product_id: str, new_price: float):
    return update_product_price(product_id, new_price)

@router.put("/products/description/{product_id}/{new_description}")
async def update_description(product_id: str, new_description: str):
    return update_product_description(product_id, new_description)

@router.put("/products/categories/{product_id}/{new_category}")
async def update_categories(product_id: str, new_category: str):
    return update_product_categories(product_id, new_category)

@router.delete("/products/{product_id}")
async def delete_product(product_id: str):
    return delete_product_by_id(product_id)

@router.get("/products/{product_id}")
async def get_product(product_id: str):
    return get_product_by_id(product_id)

@router.post("/register-category")
async def register_category(category: Category):
    return register_new_category(category)

#------------------------CATEGORIA--------------------------

@router.get("/categories")
async def categories():
    return get_all_categories()

@router.post("/register-category")
async def register_category(category: Category):
    return register_new_category(category) 

@router.get("/categories/{category_id}")
async def get_category(category_id: str):
    return get_category_by_id_controller(category_id)

@router.delete("/categories/{category_id}")
async def delete_category(category_id: str):
    return delete_category_controller(category_id)

@router.put("/categories/name/{category_id}/{new_name}")
async def update_category_name(category_id: str, new_name: str):
    return update_category_name_controller(category_id, new_name)

'''@router.get("/default-categories")
async def get_default_categories():
    return get_default_categories_controller()'''

#-----------------TABLES------------------------
@router.get("/tables")
async def tables():
    return get_tables_controller()

@router.get("/tables/{table_id}")
async def get_table(table_id: str):
    return get_table_by_id_controller(table_id)

@router.put("/tables/status/{table_id}")
async def update_table_status(table_id: str, new_status: str):
    return update_table_status_controller(table_id, new_status)

@router.put("/tables/order/{table_id}")
async def associate_order_with_table(table_id: str, order_id: int):
    return associate_order_with_table_controller(table_id, order_id)

#----------------ORDER-------------------------

@router.get("/orders")
async def orders():
    return get_orders()

@router.post("/register-order")
async def register_order(order: Order):
    print(order)
    return register_new_order(order) 

@router.put("/orders/finalize/{order_id}")
async def finalize_order(order_id: str):
    return finalize_order_controller(order_id)

@router.get("/orders/{order_id}")
async def get_order(order_id: str):
    return get_order_controller(order_id)

@router.put("/orders/order-items/{order_id}")
async def update_order_items(order_id: str, body: Dict[str, Any]):
    new_order_items = body.get("new_order_items", [])
    total = body.get("total", "")
    
    return add_order_items(order_id, new_order_items, total)
#----------------ORDERITEM-------------------------


#-----------------CALORIES----------------------

@router.put("/add-calories/{product_id}/{calories}")
async def add_calories(product_id: str, calories: float):
    return add_food_calories(product_id, calories)