from datetime import date
from pydantic import BaseModel

# Modelo para iniciar sesión
class UserLogin(BaseModel):
    email: str
    password: str

# Modelo para registrar un nuevo usuario
class UserRegister(BaseModel):
    uid: str
    name: str
    birthday: str
    imageUrl: str

# Modelo para recuperación de contraseña
class UserForgotPassword(BaseModel):
    email: str

class TokenData(BaseModel):
    id_token: str

