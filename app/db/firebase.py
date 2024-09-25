import json
from dotenv import load_dotenv
import os
from firebase_admin import credentials, firestore, initialize_app

# Cargar variables de entorno
load_dotenv()

def init_firebase():
    cred_path = os.getenv("FIREBASE_CRED_PATH")
    firebase_creds_dict = json.loads(cred_path)
    print(f"Ruta del archivo de credenciales: {cred_path}")
    cred = credentials.Certificate(firebase_creds_dict)
    initialize_app(cred)
    return firestore.client()

# Crear una instancia del cliente de Firestore
db = init_firebase()
