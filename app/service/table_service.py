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

def associate_order_with_table(table_id: str, order_id: int):
    """
    Servicio para asociar un order ID con una tabla.
    """
    print(table_id)
    print(order_id)
    try:
        table_ref = db.collection('tables').document(table_id)
        print(table_ref)
        if table_ref.get().exists:
            table_ref.update({"order_id": order_id})  # Assuming order_id is a field in your table document
            return {"message": "Order associated with table successfully"}
        else:
            return {"error": "Table not found"}
    except Exception as e:
        return {"error": str(e)}

def close_table_service(table_id: str):
    """
    Update the status of the table to 'FREE' and set order_id to 0.
    """
    try:
        table_ref = db.collection('tables').document(str(table_id))
        table_doc = table_ref.get()

        if not table_doc.exists:
            raise HTTPException(status_code=404, detail="Table not found")

        # Update the table
        table_ref.update({
            "status": "FREE",  # Set status to 'FREE'
            "order_id": 0      # Set order_id to 0
        })

        return {"message": "Table closed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))