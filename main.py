from fastapi import FastAPI
from app.api import router as user_router

app = FastAPI()

# Incluye las rutas del API de usuario
app.include_router(user_router, prefix="/user")

@app.get("/")
def root():
    return {"message": "Hello World"}
