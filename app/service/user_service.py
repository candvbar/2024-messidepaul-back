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
                    # Crear una lista que contenga el ID y el nombre del nivel
                    user_data['level'] = {
                        'id': level_id,  # ID del nivel
                        'name': level_data.get("name")  # Nombre del nivel
                    }
            
            return user_data  # Retornar los datos del usuario, ahora con el nivel incluido
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

def rewards(level_id):
    try:
        # Referencia al documento del nivel
        level_ref = db.collection('levels').document(level_id)
        level_doc = level_ref.get()  # Obtener el documento del nivel
        
        if level_doc.exists:  # Verificar si el nivel existe
            level_data = level_doc.to_dict()
            rewards_ids = level_data.get("rewards", "").split(", ")  # Obtener y dividir los IDs de rewards
            
            rewards_list = []  # Lista para almacenar los datos de cada recompensa
            for reward_id in rewards_ids:
                # Referencia al documento de cada recompensa
                reward_ref = db.collection('rewards').document(reward_id)
                reward_doc = reward_ref.get()
                
                if reward_doc.exists:  # Verificar si la recompensa existe
                    rewards_list.append(reward_doc.to_dict())  # Agregar los datos de la recompensa a la lista
            
            return rewards_list # Retornar las recompensas como un diccionario
        else:
            return {"error": "Level not found"}
    except Exception as e:
        return {"error": str(e)}

def level(level_id):
    try:
        # Referencia al documento del nivel
        level_ref = db.collection('levels').document(level_id)
        level_doc = level_ref.get()  # Obtener el documento del siguiente nivel
        
        if level_doc.exists:  # Verificar si el nivel existe
            level_data = level_doc.to_dict()
            return level_data
        else:
            return {"error": "Level not found"}
    except Exception as e:
        return {"error": str(e)}

def check_level(uid):
    try:
        # Reference to the user's document
        user_ref = db.collection('users').document(uid)
        user_doc = user_ref.get()  # Get the document
        
        if user_doc.exists:  # Check if the document exists
            user_data = user_doc.to_dict()  # Get data as a dictionary
            
            # Get the user's current level as a string and convert it to int
            current_level = int(user_data.get("level", "1"))  # Default to level 1 if missing
            current_global_points = int(user_data.get("globalPoints", "0"))  # Convert to int
            
            # Get the points required for the next level from the levels collection
            next_level_ref = db.collection("levels").document(str(current_level + 1)).get()
            
            if next_level_ref.exists:
                next_level_data = next_level_ref.to_dict()
                # Convert points required for the next level to int
                next_level_points_required = int(next_level_data['points'])  # Convert to int
                
                # Check if user qualifies for the next level
                if current_global_points >= next_level_points_required:
                    # Update user's level to the next level (convert back to string)
                    new_level = current_level + 1
                    user_ref.update({"level": str(new_level)})
                    # Update the user_data to reflect the new level
                    user_data["level"] = str(new_level)
                    user_data["level_updated"] = True  # Flag to indicate level was updated
                else:
                    user_data["level_updated"] = False  # No level change
                
            # Return user data with level update status
            return user_data
        else:
            return {"error": "User not found"}
    except Exception as e:
        return {"error": str(e)}

def get_top_level_status(level_id):
    try:
        # Stream all levels from Firestore
        levels_ref = db.collection('levels').stream()
        
        # Collect level IDs, converting them to integers for comparison
        levels_list = []
        for level in levels_ref:
            level_data = level.to_dict()
            level_data['id'] = level.id  # Use document ID as the level ID
            levels_list.append(int(level_data['id']))
        print(levels_list)
        # Ensure there are valid level IDs to compare
        if not levels_list or (int(level_id) not in levels_list):
            return {"error": "No levels found or levels have invalid IDs."}
        
        # Find the highest level ID
        max_level_id = max(levels_list)
        
        # Check if the provided level_id (converted to int) is the highest level
        return {"isTopLevel": int(level_id) == max_level_id}
    
    except ValueError:
        return {"error": "Invalid level ID format, unable to convert to integer."}
    except Exception as e:
        return {"error": str(e)}

'''def reset_monthly_points():
    """
    Resets monthly points for all users in the Firestore database.
    """
    users_ref = db.collection("users").stream()
    for user in users_ref:
        user_ref = db.collection("users").document(user.id)
        user_ref.update({"monthlyPoints": "0"})  # Resetting to zero'''