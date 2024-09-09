import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from api import router  # Importamos el router de las rutas

client = TestClient(router)

class TestProductEndpoints(unittest.TestCase):

    @patch("app.controller.product_controller.create_product")
    def test_register_product(self, mock_create_product):
    # Simular la respuesta del controlador con el ID del producto
        mock_create_product.return_value = {"id": "UhxKisSzmmp2zMmDah8N"}

        # Datos del producto de prueba
        new_product_data = {
            "description": "A new product",
            "product_name": "Product 1",
            "product_price": 100.00
        }

        # Realizar la petición POST para registrar un producto
        response = client.post("/register-product", json=new_product_data)

        # Verificar que la respuesta sea exitosa y tenga el product_id
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "message": "Product registered successfully",
            "product_id": "UhxKisSzmmp2zMmDah8N"
        })

    @patch("app.controller.product_controller.products")
    def test_get_products(self, mock_get_products):
    # Ajustar la respuesta mock a lo esperado
        mock_get_products.return_value = [
            {
                "description": "A product",
                "product_name": "Product 1",
                "product_price": 100.00
            }
        ]

        response = client.get("/products")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "message": [
                {
                    "description": "A product",
                    "product_name": "Product 1",
                    "product_price": 100.00
                }
            ]
        })


    @patch("app.controller.product_controller.update_product_newprice")
    def test_update_product_price(self, mock_update_product_price):
        # Simular la respuesta del controlador
        mock_update_product_price.return_value = {}

        # Realizar la petición PUT con el precio como parámetro de query
        response = client.put("/products/1/price?new_price=150.00")

        # Verificar que la respuesta sea exitosa
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Product price updated successfully"})


    @patch("app.controller.product_controller.delete")
    def test_delete_product(self, mock_delete_product):
        # Simular la respuesta del controlador
        mock_delete_product.return_value = {"message": "Product deleted successfully"}

        # Realizar la petición DELETE para eliminar un producto
        response = client.delete("/products/1")

        # Verificar que la respuesta sea exitosa
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Product deleted successfully"})
    
    '''@patch("app.controller.product_controller.create_product")
    def test_register_product_missing_fields(self, mock_create_product):
        # Datos incompletos (falta product_price)
        new_product_data = {
            "description": "A product without price",
            "product_name": "Product 2"
        }
        
        # Realizar la petición POST para registrar un producto con datos faltantes
        response = client.post("/register-product", json=new_product_data, headers={"Content-Type": "application/json"})
        
        # Verificar que el código de estado es 422
        self.assertEqual(response.status_code, 422)
        
        # Verificar el mensaje de error
        errors = response.json().get("detail", [])
        self.assertTrue(any(
            error['loc'] == ['body', 'product_price'] and
            error['msg'] == 'Field required'
            for error in errors
        ))'''




if __name__ == "__main__":
    unittest.main()
