from app.service.user_service import create_user, get_user_by_email, forgot_password
from app.models.user import UserLogin, UserRegister, UserForgotPassword
from fastapi import HTTPException

# Controlador para iniciar sesión
def login(user: UserLogin):
    db_user = get_user_by_email(user.email)
    if db_user and db_user["password"] == user.password:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")

# Controlador para registrar un nuevo usuario
def register(user: UserRegister):
    existing_user = get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_data = user.dict()
    response = create_user(user_data)
    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])
    return {"message": "User registered successfully", "user_id": response["id"]}

# Controlador para recuperación de contraseña
def handle_forgot_password(user: UserForgotPassword):
    db_user = get_user_by_email(user.email)
    if db_user:
        return forgot_password(user.email)
    else:
        raise HTTPException(status_code=404, detail="Email not found")
