from app.service.user_service import create_user, get_user_by_email, forgot_password, user_by_id, delete_user
from app.models.user import UserLogin, UserRegister, UserForgotPassword
from fastapi import HTTPException

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

def delete_user_by_id(uid: str):
    response = delete_user(uid)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "Product deleted successfully"}