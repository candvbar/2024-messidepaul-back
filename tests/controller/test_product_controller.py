from unittest.mock import patch
import pytest
from fastapi import HTTPException
from app.controller.product_controller import register_new_product, get_products, update_product_price, update_product_description, delete_product_by_id, get_product_by_id
from app.models.product import Product
from tests.test_util import create_test_product

class TestProductController:

    @patch('app.controller.product_controller.create_product')
    def test_register_new_product_success(self, mock_create_product):
        mock_create_product.return_value = {"message": "Product added successfully", "id": "123"}

        response = register_new_product(create_test_product())

        assert response["message"] == "Product registered successfully"
        assert response["id"] == "123"
    
    @patch('app.controller.product_controller.create_product')
    def test_register_new_product_creation_failure(self, mock_create_product):
        # Simulate an error response from create_product
        mock_create_product.return_value = {"error": "Failed to create product"}

        product = create_test_product()  # Assuming this creates a valid product

        with pytest.raises(HTTPException) as exc_info:
            register_new_product(product)

        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Failed to create product"


    @patch('app.controller.product_controller.create_product')
    def test_register_new_product_negative_price(self, mock_create_product):
        product = Product(name='Product Test', price=-10.99, description='This is a test product', category=1)

        with pytest.raises(HTTPException) as exc_info:
            register_new_product(product)

        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Price cannot be negative or zero"
    
    @patch('app.controller.product_controller.create_product')
    def test_register_new_product_string_price(self, mock_create_product):
        product = Product(name='Product Test', price="holaaaa", description='This is a test product', category=1)

        with pytest.raises(HTTPException) as exc_info:
            register_new_product(product)

        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Price must be a number"

    @patch('app.controller.product_controller.products')
    def test_get_products_success(self, mock_products):
        mock_products.return_value = {"products": [{"id": "123", "name": "Product 1"}], "message": "Products retrieved successfully"}

        response = get_products()
        assert "message" in response

    @patch('app.controller.product_controller.products')
    def test_get_products_failure(self, mock_products):
        mock_products.side_effect = Exception("Database error")

        with pytest.raises(HTTPException) as exc_info:
            get_products()

        assert exc_info.value.status_code == 500
        assert "Database error" in str(exc_info.value.detail)

    @patch('app.controller.product_controller.update_product_newprice')
    def test_update_product_price_success(self, mock_update_price):
        mock_update_price.return_value = {"message": "Product price updated successfully"}

        response = update_product_price("valid_product_id", 15.99)
        assert response["message"] == "Product price updated successfully"

    @patch('app.controller.product_controller.update_product_newprice')
    def test_update_product_price_failure(self, mock_update_price):
        mock_update_price.side_effect = Exception("Update error")

        with pytest.raises(HTTPException) as exc_info:
            update_product_price("valid_product_id", 15.99)

        assert exc_info.value.status_code == 500
        assert "Update error" in str(exc_info.value.detail)

    @patch('app.controller.product_controller.update_product_newdescription')
    def test_update_product_description_success(self, mock_update_description):
        mock_update_description.return_value = {"message": "Product description updated successfully"}

        response = update_product_description("valid_product_id", "Updated description")
        assert response["message"] == "Product description updated successfully"

    @patch('app.controller.product_controller.update_product_newdescription')
    def test_update_product_description_failure(self, mock_update_description):
        mock_update_description.side_effect = Exception("Update error")

        with pytest.raises(HTTPException) as exc_info:
            update_product_description("valid_product_id", "Updated description")

        assert exc_info.value.status_code == 500
        assert "Update error" in str(exc_info.value.detail)

    @patch('app.controller.product_controller.delete_product')
    def test_delete_product_by_id_success(self, mock_delete_product):
        mock_delete_product.return_value = {"message": "Product deleted successfully"}

        response = delete_product_by_id("valid_product_id")
        assert response is None  # Assuming no return value on success

    @patch('app.controller.product_controller.delete_product')
    def test_delete_product_by_id_failure(self, mock_delete_product):
        mock_delete_product.side_effect = ValueError("Product not found")

        with pytest.raises(HTTPException) as exc_info:
            delete_product_by_id("invalid_product_id")

        assert exc_info.value.status_code == 404
        assert "Product not found" in str(exc_info.value.detail)

    @patch('app.controller.product_controller.product_by_id')
    def test_get_product_by_id_success(self, mock_product_by_id):
        mock_product_by_id.return_value = {"product": {"id": "valid_product_id", "name": "Product Test"}, "message": "Product retrieved successfully"}

        response = get_product_by_id("valid_product_id")
        assert "message" in response

    @patch('app.controller.product_controller.product_by_id')
    def test_get_product_by_id_failure(self, mock_product_by_id):
        mock_product_by_id.return_value = {"error": "Product not found"}  # No hay cambios aquí
        
        with pytest.raises(HTTPException) as exc_info:
            get_product_by_id("invalid_product_id")
        
        assert exc_info.value.status_code == 404
        assert "Product not found" in str(exc_info.value.detail)

    @patch('app.controller.product_controller.delete_product')
    def test_delete_product_by_id_failure_general_exception(self, mock_delete_product):
        # Simulate a general exception being raised by delete_product
        mock_delete_product.side_effect = Exception("Unexpected error occurred")

        with pytest.raises(HTTPException) as exc_info:
            delete_product_by_id("valid_product_id")

        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Unexpected error occurred"

    @patch('app.controller.product_controller.product_by_id')
    def test_get_product_by_id_failure_general_exception(self, mock_product_by_id):
        # Simulate a general exception being raised by product_by_id
        mock_product_by_id.side_effect = Exception("Unexpected error occurred")

        with pytest.raises(HTTPException) as exc_info:
            get_product_by_id("valid_product_id")

        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Unexpected error occurred"
