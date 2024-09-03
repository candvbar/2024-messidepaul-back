from app.db.firebase import db
from firebase_admin import firestore

# Crear un nuevo usuario en Firestore
def create_user(user_data):
    try:
        new_user_ref = db.collection('users').document()
        new_user_ref.set(user_data)
        return {"message": "User added successfully", "id": new_user_ref.id}
    except Exception as e:
        return {"error": str(e)}

# Obtener un usuario por su email
def get_user_by_email(email):
    try:
        users_ref = db.collection('users')
        query = users_ref.where('email', '==', email).stream()

        for user in query:
            return user.to_dict()
        return None
    except Exception as e:
        return {"error": str(e)}

# Función para manejar la recuperación de contraseña
def forgot_password(email):
    # Simulamos que mandamos un correo de recuperación
    return {"message": f"Password reset link sent to {email}"}
