# tests/test_mechanics.py

import unittest
from app import create_app, db
from app.models import Mechanic

class TestMechanicEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app(testing=True)  # FIXED: create the app with test config
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_mechanic(self):
        payload = {
    "name": "Tyrone Wrenchman",
    "phone": "555-9876",
    "email": "tyrone@example.com",
    "salary": 55000.0
}


        response = self.client.post("/mechanics/", json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertIn("name", response.get_json())
        self.assertEqual(response.get_json()["name"], "Tyrone Wrenchman")

if __name__ == '__main__':
    unittest.main()

