from fastapi import APIRouter
from app.models.user import UserLogin, UserRegister, UserForgotPassword
from app.models.product import Product
from app.controller.user_controller import login, register, handle_forgot_password
from app.controller.product_controller import register_new_product, get_products, update_product_price, update_product_description, delete, get_product_by_id

router = APIRouter()

@router.get("/")
async def root():
    return "Server is running"

# Ruta para iniciar sesión
@router.post("/login/")
async def login_user(user: UserLogin):
    return login(user)

# Ruta para registrar un nuevo usuario
@router.post("/register/")
async def register_user(user: UserRegister):
    return register(user)

# Ruta para recuperación de contraseña
@router.post("/forgot-password/")
async def forgot_password_user(user: UserForgotPassword):
    return handle_forgot_password(user)

@router.post("/register-product")
async def register_product(product: Product):
    return register_new_product(product)

@router.get("/products")
async def products():
    return get_products()

@router.put("/products/{product_id}/price")
async def update_price(product_id: str, new_price: float):
    return update_product_price(product_id, new_price)

@router.put("/products/{product_id}/description")
async def update_description(product_id: str, new_description: str):
    return update_product_description(product_id, new_description)

@router.delete("/products/{product_id}")
async def delete_product(product_id: str):
    return delete(product_id)

@router.get("/products/{product_id}")
async def get_product(product_id: str):
    return get_product_by_id(product_id)