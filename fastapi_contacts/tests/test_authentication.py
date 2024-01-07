# tests/test_authentication.py

import unittest
from fastapi.testclient import TestClient
from fastapi_contacts.main import app
from fastapi_contacts.app.models import User
from fastapi_contacts.app.database import SessionLocal

class TestAuthentication(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.test_user = {"email": "test@example.com", "password": "testpassword"}

    def tearDown(self):
        # Clean up any test data
        db = SessionLocal()
        user = db.query(User).filter(User.email == self.test_user["email"]).first()
        if user:
            db.delete(user)
            db.commit()
        db.close()

    def test_register_user(self):
        response = self.client.post("/register", json=self.test_user)
        assert response.status_code == 200  # Updated assertion
        assert response.json()["email"] == self.test_user["email"]

    def test_login_for_access_token(self):
        # Register a test user first
        self.client.post("/register", json=self.test_user)

        # Log in and get an access token
        response = self.client.post("/token",
                                    data={"username": self.test_user["email"], "password": self.test_user["password"]})
        assert response.status_code == 200, f"Login failed with status code {response.status_code}. Response text: {response.text}"
        assert "access_token" in response.json(), f"Expected 'access_token' in response, but it was not found. Response json: {response.json()}"

    def test_read_users_me(self):
        # Register a test user first
        self.client.post("/register", json=self.test_user)

        # Log in and get an access token
        response = self.client.post("/token",
                                    data={"username": self.test_user["email"], "password": self.test_user["password"]})
        assert response.status_code == 200, f"Login failed with status code {response.status_code}. Response text: {response.text}"
        assert "access_token" in response.json(), f"Expected 'access_token' in response, but it was not found. Response json: {response.json()}"

        # Use the access token to get user information
        response = self.client.get("/users/me", headers={"Authorization": f"Bearer {response.json()['access_token']}"})
        assert response.status_code == 200, f"Failed to get user information with status code {response.status_code}. Response text: {response.text}"
        assert response.json()["email"] == self.test_user[
            "email"], f"Expected email '{self.test_user['email']}' but got '{response.json()['email']}'. Response json: {response.json()}"

