from unittest.mock import patch
import pytest
from app.service.product_service import create_product, products, update_product_newprice, update_product_newdescription, delete_product, product_by_id

class TestProductService:

    @patch('app.db.firebase.db')
    def test_create_product_success(self, mock_db):
        mock_new_product_ref = mock_db.collection.return_value.document.return_value
        mock_new_product_ref.id = "123"
        
        mock_db.collection.return_value.document.return_value.set.return_value = None

        response = create_product({"name": "Product Test", "price": 10.99, "description": "This is a test product", "category": 1})

        assert response["message"] == "Product added successfully"
        assert response["id"] == "123"

    @patch('app.db.firebase.db')
    def test_products_success(self, mock_db):
        mock_product_ref = mock_db.collection.return_value.stream.return_value
        mock_product_ref.__iter__.return_value = [mock_product_ref]

        response = products()
        assert "products" in response

    @patch('app.db.firebase.db')
    def test_update_product_newprice_success(self, mock_db):
        mock_db.collection.return_value.document.return_value.update.return_value = None

        response = update_product_newprice("valid_product_id", 15.99)
        assert response["message"] == "Product price updated successfully"

    @patch('app.db.firebase.db')
    def test_update_product_newdescription_success(self, mock_db):
        mock_db.collection.return_value.document.return_value.update.return_value = None

        response = update_product_newdescription("valid_product_id", "Updated description")
        assert response["message"] == "Product description updated successfully"

    @patch('app.db.firebase.db')
    def test_delete_product_success(self, mock_db):
        mock_product_ref = mock_db.collection.return_value.document.return_value
        mock_product_ref.get.return_value.exists = True

        response = delete_product("valid_product_id")
        assert response["message"] == "Product deleted successfully"

    @patch('app.db.firebase.db')
    def test_product_by_id_success(self, mock_db):
        mock_product_ref = mock_db.collection.return_value.document.return_value
        mock_product_ref.get.return_value.exists = True
        mock_product_ref.get.return_value.to_dict.return_value = {"name": "Product Test", "price": 10.99}

        response = product_by_id("valid_product_id")
        assert "product" in response
