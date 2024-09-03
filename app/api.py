from fastapi import APIRouter
from app.models.user import UserLogin, UserRegister, UserForgotPassword
from app.controller.user_controller import login, register, handle_forgot_password

router = APIRouter()

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
