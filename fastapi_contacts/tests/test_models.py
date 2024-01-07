# fastapi_contacts/tests/test_models.py

import unittest
from fastapi_contacts.app.models import Contact, User

class TestContactModel(unittest.TestCase):

    def test_contact_model(self):
        # Create a Contact instance
        contact = Contact(
            name="John",
            surname="Doe",
            email="john.doe@example.com",
            phone_number="123456789",
            birthday="1990-01-01",
            additional_info="Additional information"
        )

        # Check if attributes are set correctly
        self.assertEqual(contact.name, "John")
        self.assertEqual(contact.surname, "Doe")
        self.assertEqual(contact.email, "john.doe@example.com")
        self.assertEqual(contact.phone_number, "123456789")
        self.assertEqual(contact.birthday, "1990-01-01")
        self.assertEqual(contact.additional_info, "Additional information")

class TestUserModel(unittest.TestCase):

    def test_user_model(self):
        # Create a User instance
        user = User(
            email="testuser@example.com",
            hashed_password="hashed_password",
            is_active=True,
            access_token="access_token",
            refresh_token="refresh_token",
            email_verified=True
        )

        # Check if attributes are set correctly
        self.assertEqual(user.email, "testuser@example.com")
        self.assertEqual(user.hashed_password, "hashed_password")
        self.assertTrue(user.is_active)
        self.assertEqual(user.access_token, "access_token")
        self.assertEqual(user.refresh_token, "refresh_token")
        self.assertTrue(user.email_verified)

if __name__ == '__main__':
    unittest.main()
