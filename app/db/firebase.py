from firebase_admin import credentials, firestore, initialize_app

# Inicializar Firebase
def init_firebase():
    cred = credentials.Certificate("candvbar-firebase-adminsdk-fzqx8-ab3c591562.json")
    initialize_app(cred)
    return firestore.client()

# Crear una instancia del cliente de Firestore
db = init_firebase()
