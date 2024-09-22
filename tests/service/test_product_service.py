from unittest.mock import MagicMock, patch
import pytest
from app.service.product_service import (
    create_product, products, update_product_newprice, 
    update_product_newdescription, delete_product, product_by_id
)
from tests.test_util import create_test_product

class TestProductService:
    
    @patch('app.service.product_service.db')  # Esto pasa 'mock_db' como argumento
    def test_create_product_success(self, mock_db):
        mock_document_ref = MagicMock()
        mock_document_ref.id = '123'
        mock_db.collection.return_value.document.return_value = mock_document_ref
        
        test_product = create_test_product()
        product_data = {
            "name": test_product.name,
            "price": test_product.price,
            "description": test_product.description,
            "category": test_product.category,
        }

        response = create_product(product_data)
        
        mock_document_ref.set.assert_called_once_with(product_data)
        assert response["id"] == '123'
        assert response["message"] == "Product added successfully"

    @patch('app.service.product_service.db')  # Ajuste para evitar acceso a la BDD
    def test_products_success(self, mock_db):
        mock_product_ref = MagicMock()
        mock_product_ref.to_dict.return_value = {
            "name": "Product Test", 
            "price": 10.99, 
            "description": "Test description", 
            "category": 1
        }

        mock_db.collection.return_value.stream.return_value = [mock_product_ref]

        response = products()
        assert "products" in response
        assert len(response["products"]) == 1
        assert response["products"][0]["name"] == "Product Test"

    @patch('app.service.product_service.db')  # Ajuste para evitar acceso a la BDD
    def test_update_product_newprice_success(self, mock_db):
        # Aquí se necesita verificar el mock del documento que se actualiza en la función
        mock_document_ref = mock_db.collection.return_value.document.return_value

        # Simula que la actualización fue exitosa
        response = update_product_newprice("valid_product_id", 15.99)
        
        # Verifica que se haya llamado a la función update con los datos correctos
        mock_document_ref.update.assert_called_once_with({"price": 15.99})
        assert response["message"] == "Product price updated successfully"

    @patch('app.service.product_service.db')  # Ajuste para evitar acceso a la BDD
    def test_update_product_newdescription_success(self, mock_db):
        # Igual que el test anterior, necesitamos el mock correcto
        mock_document_ref = mock_db.collection.return_value.document.return_value

        # Simula que la actualización fue exitosa
        response = update_product_newdescription("valid_product_id", "Updated description")
        
        # Verifica que se haya llamado a la función update con los datos correctos
        mock_document_ref.update.assert_called_once_with({"description": "Updated description"})
        assert response["message"] == "Product description updated successfully"

    @patch('app.service.product_service.db')  # Ajuste para evitar acceso a la BDD
    def test_delete_product_success(self, mock_db):
        mock_document_ref = mock_db.collection.return_value.document.return_value
        mock_document_ref.get.return_value.exists = True

        response = delete_product("valid_product_id")
        mock_document_ref.delete.assert_called_once()
        assert response["message"] == "Product deleted successfully"

    @patch('app.service.product_service.db')  # Ajuste para evitar acceso a la BDD
    def test_product_by_id_success(self, mock_db):
        mock_document_ref = mock_db.collection.return_value.document.return_value
        mock_document_ref.get.return_value.exists = True
        mock_document_ref.get.return_value.to_dict.return_value = {
            "name": "Product Test", 
            "price": 10.99, 
            "description": "Test description", 
            "category": 1
        }

        response = product_by_id("valid_product_id")
        assert "product" in response
        assert response["product"]["name"] == "Product Test"
        assert response["product"]["price"] == 10.99
