from app.db.firebase import db

def create_product(product_data):
    try:
        new_product_ref = db.collection('products').document()
        new_product_ref.set(product_data)
        return {"message": "Product added successfully", "id": new_product_ref.id}
    except Exception as e:
        return {"error": str(e)}

def products():
    try:
        products_ref = db.collection('products')
        products = products_ref.stream()
        product_list = []

        for product in products:
            product_dict = product.to_dict()
            product_dict['id'] = product.id
            product_list.append(product_dict)
            
        return {"products": product_list, "message": "Products retrieved successfully"}
    except Exception as e:
        return {"error": str(e)}  # Removed the status code tuple


def update_product_newprice(product_id: str, new_price: float):
    try:
        product_ref = db.collection('products').document(product_id)
        product_ref.update({"product_price": new_price})
        return {"message": "Product price updated successfully"}
    except Exception as e:
        return {"error": str(e)}


def update_product_newdescription(product_id, new_description):
    try:
        # Referencia al documento del producto que se va a actualizar
        product_ref = db.collection('products').document(product_id)

        # Actualización solo del campo 'description'
        product_ref.update({
            'description': new_description
        })

        return {"message": "Product description updated successfully"}
    except Exception as e:
        return {"error": str(e)}

def delete_product(product_id: str):
    product_ref = db.collection('products').document(product_id)
    product_doc = product_ref.get()
    if not product_doc.exists:
        raise ValueError("Product not found")
    product_ref.delete()
    return {"message": "Product deleted successfully"}


def product_by_id(product_id: str):
    try:
        # Retrieve the document reference
        product_ref = db.collection('products').document(product_id)
        product_doc = product_ref.get()

        if not product_doc.exists:
            return {"error": "Product not found"}
        
        product_data = product_doc.to_dict()
        product_data['id'] = product_id
        
        return {"product": product_data, "message": "Product retrieved successfully"}
    except Exception as e:
        return {"error": str(e)}
