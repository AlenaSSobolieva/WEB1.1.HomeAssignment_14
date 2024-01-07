import unittest
import uuid  # Add this line
from fastapi.testclient import TestClient
from fastapi_contacts.main import app
from fastapi_contacts.app.models import Contact
from fastapi_contacts.app.database import SessionLocal

class TestContacts(unittest.TestCase):

    def setUp(self):
        # Adjust the base_url to the root path
        self.client = TestClient(app, base_url="http://127.0.0.1:8000")
        # Use a dynamic or unique email for each test run
        self.test_contact = {
            "name": "John Doe",
            "email": f"john.doe.{uuid.uuid4()}@example.com",  # Fix the uuid import
            "password": "Queen2001)"
        }

    def tearDown(self):
        # Clean up any test data
        db = SessionLocal()

        # Retrieve the contact by email
        contact = db.query(Contact).filter(Contact.email == self.test_contact["email"]).first()

        if contact:
            db.delete(contact)
            db.commit()

        db.close()

    def test_register_contact(self):
        # Register a test contact first
        response = self.client.post("/contacts/register", json=self.test_contact)
        assert response.status_code == 201, f"Unexpected status code: {response.status_code}\nResponse content: {response.text}"
        assert response.json()["email"] == self.test_contact["email"]

        # Try to register the same contact again
        response = self.client.post("/contacts/register", json=self.test_contact)
        assert response.status_code == 409, f"Unexpected status code: {response.status_code}\nResponse content: {response.text}"
        assert "User already registered with this email" in response.json()["detail"]

        # Print the response content for debugging
        print(response.text)

