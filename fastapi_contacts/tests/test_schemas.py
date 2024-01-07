# fastapi_contacts/tests/test_schemas.py

import unittest
from fastapi_contacts.app.schemas import (
    OAuth2PasswordRequestForm,
    UserBase,
    UserCreate,
    UserResponse,
    Contact,
    Token,
    Message,
)

class TestSchemas(unittest.TestCase):

    def test_oauth2_password_request_form(self):
        data = {
            "email": "test@example.com",
            "password": "password123",
            "scope": "read write",
            "client_id": "client123",
            "client_secret": "secret123",
            "grant_type": "password",
        }
        form = OAuth2PasswordRequestForm(**data)

        self.assertEqual(form.username, data["email"])
        self.assertEqual(form.password, data["password"])
        self.assertEqual(form.scope, data["scope"])
        self.assertEqual(form.client_id, data["client_id"])
        self.assertEqual(form.client_secret, data["client_secret"])
        self.assertEqual(form.grant_type, data["grant_type"])

    def test_user_base(self):
        data = {
            "id": 1,
            "email": "user@example.com",
            "is_active": True,
            "avatar_url": "http://example.com/avatar.jpg",
        }
        user_base = UserBase(**data)

        self.assertEqual(user_base.id, data["id"])
        self.assertEqual(user_base.email, data["email"])
        self.assertEqual(user_base.is_active, data["is_active"])
        self.assertEqual(user_base.avatar_url, data["avatar_url"])

    def test_user_create(self):
        data = {
            "id": 1,
            "email": "user@example.com",
            "is_active": True,
            "avatar_url": "http://example.com/avatar.jpg",
            "password": "password123",
        }
        user_create = UserCreate(**data)

        self.assertEqual(user_create.id, data["id"])
        self.assertEqual(user_create.email, data["email"])
        self.assertEqual(user_create.is_active, data["is_active"])
        self.assertEqual(user_create.avatar_url, data["avatar_url"])
        self.assertEqual(user_create.password, data["password"])

    def test_user_response(self):
        data = {
            "id": 1,
            "email": "user@example.com",
            "is_active": True,
        }
        user_response = UserResponse(**data)

        self.assertEqual(user_response.id, data["id"])
        self.assertEqual(user_response.email, data["email"])
        self.assertEqual(user_response.is_active, data["is_active"])

    def test_contact(self):
        data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "password": "contact_password",
        }
        contact = Contact(**data)

        self.assertEqual(contact.name, data["name"])
        self.assertEqual(contact.email, data["email"])
        self.assertEqual(contact.password, data["password"])

    def test_token(self):
        data = {
            "access_token": "access_token_value",
            "token_type": "bearer",
        }
        token = Token(**data)

        self.assertEqual(token.access_token, data["access_token"])
        self.assertEqual(token.token_type, data["token_type"])

    def test_message(self):
        data = {
            "message": "Test message content",
        }
        message = Message(**data)

        self.assertEqual(message.message, data["message"])

if __name__ == '__main__':
    unittest.main()
