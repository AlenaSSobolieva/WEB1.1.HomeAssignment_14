# tests/test_crud.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from fastapi_contacts.app.crud import create_user, get_user_by_email, create_contact, get_contact_by_email
from fastapi_contacts.app.models import UserCreate, Contact
from fastapi_contacts.app.database import Base
import fastapi_contacts.main

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


fastapi_contacts.main.app.dependency_overrides[override_get_db] = override_get_db
client = TestClient(fastapi_contacts.main.app)


def test_create_user():
    user_data = {"email": "test@example.com", "password": "password123"}
    user_create = UserCreate(**user_data)
    created_user = create_user(TestingSessionLocal(), user_create)
    assert created_user.email == user_data["email"]


def test_get_user_by_email():
    user_data = {"email": "test@example.com", "password": "password123"}
    user_create = UserCreate(**user_data)
    create_user(TestingSessionLocal(), user_create)
    retrieved_user = get_user_by_email(TestingSessionLocal(), user_data["email"])
    assert retrieved_user.email == user_data["email"]


def test_create_contact():
    contact_data = {"email": "contact@example.com", "name": "John Doe"}
    contact = Contact(**contact_data)
    created_contact = create_contact(TestingSessionLocal(), contact)
    assert created_contact.email == contact_data["email"]


def test_get_contact_by_email():
    contact_data = {"email": "contact@example.com", "name": "John Doe"}
    contact = Contact(**contact_data)
    create_contact(TestingSessionLocal(), contact)
    retrieved_contact = get_contact_by_email(TestingSessionLocal(), contact_data["email"])
    assert retrieved_contact.email == contact_data["email"]
