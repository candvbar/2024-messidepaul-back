from pydantic import BaseModel

# Modelo para iniciar sesión
class UserLogin(BaseModel):
    email: str
    password: str

# Modelo para registrar un nuevo usuario
class UserRegister(BaseModel):
    name: str
    email: str
    password: str

# Modelo para recuperación de contraseña
class UserForgotPassword(BaseModel):
    email: str
