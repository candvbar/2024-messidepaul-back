from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router

app = FastAPI()

origins = [
    "http://localhost:4201", 
    "https://two024-ranchoaparte-back.onrender.com",
    "http://localhost:3000",
    "https://2024-messidepaul-front.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)


# Incluir las rutas de tu API
app.include_router(router)