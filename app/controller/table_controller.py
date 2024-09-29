from app.service.table_service import get_tables_service, get_table_by_id
from app.models.table import Table
from fastapi import HTTPException


def get_tables_controller():
    """
    Controlador para obtener todas las categorías.
    """
    return get_tables_service()

def get_table_by_id_controller(table_id: str):
    """
    Controlador para obtener una categoría por ID.
    """
    table = get_table_by_id(table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return table