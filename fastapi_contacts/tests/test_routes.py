# fastapi_contacts/tests/test_routes.py

import unittest
from fastapi import UploadFile, HTTPException
from fastapi.testclient import TestClient
from fastapi_contacts.app import database
from fastapi_contacts.app.models import User
from fastapi_contacts.app.database import SessionLocal
from fastapi_contacts.app.routes import router

class TestUserRoutes(unittest.TestCase):

    def setUp(self):
        # Create a test database and client
        self.db = SessionLocal()
        self.client = TestClient(router)

    def tearDown(self):
        # Close the test database session
        self.db.close()

    def test_register_user(self):
        # Test user registration route

        # Prepare a test user
        test_user_data = {
            "email": "testuser@example.com",
            "password": "testpassword"
        }

        # Send a POST request to register the user
        response = self.client.post("/register", json=test_user_data)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the response model matches the expected UserResponse model
        response_data = response.json()
        self.assertEqual(response_data["email"], test_user_data["email"])
        self.assertTrue(response_data["is_active"])

    def test_verify_email(self):
        # Test email verification route

        # Create a test user in the database
        test_user = User(email="testuser@example.com", hashed_password="testpassword")
        self.db.add(test_user)
        self.db.commit()

        # Send a GET request to verify the email
        response = self.client.get(f"/verify-email/{test_user.id}")

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the response message indicates successful email verification
        response_data = response.json()
        self.assertEqual(response_data["message"], "Email successfully verified")

    def test_verify_email_user_not_found(self):
        # Test email verification route with user not found

        # Send a GET request to verify the email for a non-existent user
        response = self.client.get("/verify-email/999")

        # Check if the response status code is 404 (Not Found)
        self.assertEqual(response.status_code, 404)

        # Check if the response detail indicates user not found
        response_data = response.json()
        self.assertEqual(response_data["detail"], "User not found")

if __name__ == '__main__':
    unittest.main()
