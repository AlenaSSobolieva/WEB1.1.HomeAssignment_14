# fastapi_contacts/app/models.py

from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    phone_number = Column(String)
    birthday = Column(String)  # Keep it as a string
    additional_info = Column(String, nullable=True)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)  # Default to False for email verification
    access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
    email_verified = Column(Boolean, default=False)  # New field for email verification status

class UserCreate:
    email: str
    password: str
