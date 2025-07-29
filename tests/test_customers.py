import unittest
from app import create_app, db
from app.models import Customer

class TestCustomerEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app(testing=True)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_customer(self):
        payload = {
    "name": "John Doe",
    "email": "john@example.com",
    "password": "secret123",
    "phone": "555-1234"  # optional, but good to have
    }

        response = self.client.post("/customers/", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["name"], "John Doe")

if __name__ == "__main__":
    unittest.main()
