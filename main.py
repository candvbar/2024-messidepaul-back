from fastapi import FastAPI, HTTPException
from firebase_admin import credentials, firestore, initialize_app 
from pydantic import BaseModel 
from typing import Optional

app = FastAPI()

# Initialize Firebase Admin SDK
cred = credentials.Certificate("/Users/mariavictoriaheine/PID/candv-bar-firebase-adminsdk-i73u1-eca35cfad9.json")
firebase_app = initialize_app(cred)
db = firestore.client()

@app.get("/")
def root():
    return {"message": "Hello World"}

'''@app.get("/users/")
def getUsers():
    users_ref = db.collection('users')
    docs = users_ref.stream()

    users = []
    for doc in docs:
        user_data = doc.to_dict()
        users.append(user_data)

    return users'''

class User(BaseModel):
    name: str
    mail: str

@app.post("/users/")
async def create_user(user: User):
    try:
        # Generar automáticamente un nuevo documento en la colección 'users'
        new_user_ref = db.collection('users').document()
        new_user_ref.set(user.dict())
        return {"message": "User added successfully", "id": new_user_ref.id}
    except Exception as e:
        # Maneja posibles errores
        raise HTTPException(status_code=500, detail=str(e))


