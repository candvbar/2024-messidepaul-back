from dotenv import load_dotenv
import os
from firebase_admin import credentials, firestore, initialize_app

# Cargar variables de entorno
load_dotenv()

def init_firebase():
    cred_path = os.getenv('FIREBASE_CREDENTIALS')
    cred = credentials.Certificate(cred_path)
    initialize_app(cred)
    return firestore.client()

# Crear una instancia del cliente de Firestore
db = init_firebase()
