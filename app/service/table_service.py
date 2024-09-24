from app.db.firebase import db
from app.models.table import Table
from fastapi import HTTPException

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