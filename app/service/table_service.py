from app.db.firebase import db

def get_tables_service():
    """
    Servicio para obtener todas las tables desde Firebase.
    """
    try:
        tables_ref = db.collection('tables').stream()
        tables = []
        for table in tables_ref:
            tab = table.to_dict()
            tab['id'] = table.id  # Añadir el ID a la respuesta
            tables.append(tab)
        return tables
    except Exception as e:
        return {"error": str(e)}

def get_table_by_id(table_id: str):
    """
    Servicio para obtener una categoría por su ID.
    """
    try:
        table_ref = db.collection('tables').document(table_id).get()
        if table_ref.exists:
            table = table_ref.to_dict()
            table['id'] = table_ref.id
            return table
        else:
            return None  # Si la categoría no existe
    except Exception as e:
        return {"error": str(e)}

def update_table_status(table_id: str, new_status: str):
        try:
            tables_ref = db.collection('tables').document(table_id)
            if tables_ref.get().exists:
                tables_ref.update({"status": new_status})
                return {"message": "Table status updated successfully"}
            else:
                return {"error": "Table not found"}
        except Exception as e:
            return {"error": str(e)}