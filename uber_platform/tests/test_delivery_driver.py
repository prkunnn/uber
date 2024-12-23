import unittest
from app import app, get_db_connection
from werkzeug.security import generate_password_hash

class DeliveryDriverTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Add test delivery driver
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO delivery_driver (name, email, password) 
            VALUES (%s, %s, %s)
        """, ("Test Driver", "test.driver@example.com", generate_password_hash("password123")))
        conn.commit()
        self.driver_id = cursor.lastrowid
        cursor.close()
        conn.close()

    def tearDown(self):
        # Clean up database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM delivery_driver WHERE email = %s", ("test.driver@example.com",))
        conn.commit()
        cursor.close()
        conn.close()

    def test_login(self):
        response = self.app.post('/delivery_login', data={
            'email': 'test.driver@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to assigned orders

    def test_view_assigned_orders(self):
        with self.app.session_transaction() as session:
            session['driver_id'] = self.driver_id
        response = self.app.get('/assigned_orders')
        self.assertEqual(response.status_code, 200)

    def test_accept_order(self):
        with self.app.session_transaction() as session:
            session['driver_id'] = self.driver_id
        response = self.app.post('/accept_order', data={'order_id': 1})  # Example order ID
        self.assertEqual(response.status_code, 302)  # Redirect back to assigned orders

    def test_start_delivery(self):
        with self.app.session_transaction() as session:
            session['driver_id'] = self.driver_id
        response = self.app.post('/start_delivery', data={'order_id': 1})  # Example order ID
        self.assertEqual(response.status_code, 302)  # Redirect back to assigned orders

    def test_complete_order(self):
        with self.app.session_transaction() as session:
            session['driver_id'] = self.driver_id
        response = self.app.post('/complete_order', data={'order_id': 1})  # Example order ID
        self.assertEqual(response.status_code, 302)  # Redirect back to assigned orders


if __name__ == '__main__':
    unittest.main()
