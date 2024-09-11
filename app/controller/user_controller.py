from app.service.user_service import create_user, get_user_by_email, forgot_password, user_by_id
from app.models.user import UserLogin, UserRegister, UserForgotPassword
from fastapi import HTTPException

# Controlador para iniciar sesión
def login(user: UserLogin):
    return {"message": "Login successful"}
# Controlador para registrar un nuevo usuario
def register(user: UserRegister):
    response = create_user(user)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "User registered successfully"}

# Controlador para recuperación de contraseña
def handle_forgot_password(user: UserForgotPassword):
    db_user = get_user_by_email(user.email)
    if db_user:
        return forgot_password(user.email)
    else:
        raise HTTPException(status_code=404, detail="Email not found")

def get_user_by_id(uid: str):
    response = user_by_id(uid)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return response