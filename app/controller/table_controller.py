from app.service.table_service import get_tables_service
from app.models.table import Table
from fastapi import HTTPException


def get_tables_controller():
    """
    Controlador para obtener todas las categorías.
    """
    return get_tables_service()