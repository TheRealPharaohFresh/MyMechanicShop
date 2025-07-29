import unittest
from app import create_app, db
from app.models import Customer

class TestServiceTicketsEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')  # make sure you have a testing config
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            # Create a customer for FK reference
            customer = Customer(
                name="John Doe",
                email="john@example.com",
                password="secret123",
                phone="555-1234"
            )
            db.session.add(customer)
            db.session.commit()
            self.customer_id = customer.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_service_ticket(self):
        payload = {
            "customer_id": self.customer_id,
            "service_date": "2025-07-28",
            "description": "Brake replacement",
            "vin": "1HGCM82633A004352"
        }
        response = self.client.post("/service_tickets/", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["description"], "Brake replacement")
        self.assertEqual(data["vin"], "1HGCM82633A004352")
        self.assertEqual(data["customer_id"], self.customer_id)

if __name__ == '__main__':
    unittest.main()


