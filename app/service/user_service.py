from app.db.firebase import db

# Crear un nuevo usuario en Firestore
def create_user(user_data):
    try:
        doc_ref = db.collection("users").document(user_data.uid)
        doc_ref.set({
            "name": user_data.name,
            "birthday": user_data.birthday,
            "imageUrl": user_data.imageUrl,
            "level": "1",
            "globalPoints": "0",
            "monthlyPoints": "0"
        })
        return {"message": "User data saved successfully"}
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

def user_by_id(uid):
    try:
        # Referencia al documento del usuario
        user_ref = db.collection('users').document(uid)
        user_doc = user_ref.get()  # Obtener el documento
        
        if user_doc.exists:  # Verificar si el documento existe
            user_data = user_doc.to_dict()  # Obtener datos como un diccionario
            
            # Obtener el nivel del usuario
            level_id = user_data.get("level")
            if level_id:
                # Referencia al documento del nivel
                level_ref = db.collection('levels').document(level_id)
                level_doc = level_ref.get()  # Obtener el documento del nivel
                
                if level_doc.exists:  # Verificar si el documento del nivel existe
                    level_data = level_doc.to_dict()  # Obtener datos del nivel
                    user_data['level'] = level_data.get("name")  # Agregar el nombre del nivel al diccionario del usuario
            
            return user_data  # Retornar los datos del usuario, ahora con el nombre del nivel incluido
        else:
            return {"error": "User not found"}
    except Exception as e:
        return {"error": str(e)}


def delete_user(uid):
    try:
        user_ref = db.collection('users').document(uid)
        user_ref.delete()
        return {"message": "User deleted successfully"}
    except Exception as e:
        return {"error": str(e)}

def ranking():
    try:
        user_ref = db.collection('users')
        users = user_ref.stream()
        user_data = sorted(
            [
                {
                    "name": user.get("name"),
                    "imageUrl": user.get("imageUrl"),
                    "monthlyPoints": int(user.get("monthlyPoints"))
                }
                for user in users
            ],
            key=lambda x: x["monthlyPoints"],
            reverse=True
        )

        return user_data
    except Exception as e:
        return {"error": str(e)}

     