import unittest
from app import create_app, db
from app.models import Inventory

class TestInventoryEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app(testing=True)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_inventory(self):
        with self.app.app_context():
            item = Inventory(name="Oil Filter", quantity=15, price=9.99)
            db.session.add(item)
            db.session.commit()

        response = self.client.get("/inventory/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(any(i["name"] == "Oil Filter" for i in data))



if __name__ == "__main__":
    unittest.main()
