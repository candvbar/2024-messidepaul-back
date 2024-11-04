from app.service.user_service import create_user, get_user_by_email, forgot_password, ranking, rewards, user_by_id, delete_user
from app.models.user import TokenData, UserLogin, UserRegister, UserForgotPassword
from firebase_admin import auth
from fastapi import HTTPException

def login(user: UserLogin):
    try:
        # Verificar las credenciales del usuario
        user = auth.get_user_by_email(user.email)
        return {"message": "Usuario autenticado exitosamente", "user_id": user.uid}
    except firebase_admin.auth.AuthError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def token(token_data: TokenData):
    try:
        # Verificar el token enviado por el cliente
        decoded_token = auth.verify_id_token(token_data.id_token)
        uid = decoded_token['uid']
        return {"message": "Token verificado", "user_id": uid}
    except firebase_admin.auth.AuthError as e:
        raise HTTPException(status_code=400, detail="Token no válido o expirado")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

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

def ranking_controller():
    try: 
        response = ranking()
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def rewards_controller(level_id: str):
    try: 
        response = rewards(level_id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
