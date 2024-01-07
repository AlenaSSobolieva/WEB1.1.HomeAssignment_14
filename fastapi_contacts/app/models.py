# fastapi_contacts/app/models.py

from sqlalchemy import Boolean, Column, Integer, String
from fastapi_contacts.app.database import Base

class Contact(Base):
    """
    SQLAlchemy model representing a contact.

    Attributes:
    - `id` (int): Primary key.
    - `name` (str): Contact's name.
    - `surname` (str): Contact's surname.
    - `email` (str): Contact's email (unique).
    - `phone_number` (str): Contact's phone number.
    - `birthday` (str): Contact's birthday (as a string).
    - `additional_info` (str, optional): Additional information about the contact.
    """
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    phone_number = Column(String)
    birthday = Column(String)  # Keep it as a string
    additional_info = Column(String, nullable=True)

class User(Base):
    """
    SQLAlchemy model representing a user.

    Attributes:
    - `id` (int): Primary key.
    - `email` (str): User's email (unique).
    - `hashed_password` (str): Hashed user password.
    - `is_active` (bool): User's activation status (default to False for email verification).
    - `access_token` (str, optional): User's access token.
    - `refresh_token` (str, optional): User's refresh token.
    - `email_verified` (bool): User's email verification status (default to False).
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)  # Default to False for email verification
    access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
    email_verified = Column(Boolean, default=False)  # New field for email verification status

class UserCreate:
    """
    Pydantic model representing user creation request.

    Attributes:
    - `email` (str): User's email.
    - `password` (str): User's password.
    """
    email: str
    password: str
