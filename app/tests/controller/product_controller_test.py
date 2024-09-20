import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app import app  # Asegúrate de que `app` esté importado desde tu aplicación
from app.models.product import Product
from app.api import register_new_product  # Importa la función que quieres probar

# Configuramos el cliente de pruebas para FastAPI
client = TestClient(app)

class TestProductRegistration(unittest.TestCase):
    
    # Test del registro de producto usando un mock para la base de datos
    @patch('app.api.create_product')  # Mockeamos la función que interactúa con Firestore
    def test_register_product(self, mock_create_product):
        # Simulamos el comportamiento de create_product
        mock_create_product.return_value = {"message": "Product added successfully", "id": "12345"}

        # JSON del producto que vamos a enviar
        product_data = {
            "description": "This is a test product",
            "name": "Test Product",
            "price": 10.99,
            "category": 1
        }

        # Enviar la petición POST
        response = client.post("/register-product", json=product_data)

        # Validamos que la respuesta sea exitosa
        self.assertEqual(response.status_code, 200)
        self.assertIn("Product registered successfully", response.json()['message'])
        self.assertEqual(response.json()['product_id'], "12345")

        # Verificamos que create_product fue llamada con los datos correctos
        mock_create_product.assert_called_once_with(product_data)

if __name__ == "__main__":
    unittest.main()
