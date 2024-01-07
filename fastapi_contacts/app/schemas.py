# fastapi_contacts/app/schemas.py

from pydantic import BaseModel, Field
from typing import List, Optional

class OAuth2PasswordRequestForm(BaseModel):
    """
    OAuth2 Password Request Form schema.

    Attributes:
    - `username` (str): User's email (alias for username).
    - `password` (str): User's password.
    - `scope` (str, optional): OAuth2 scope (default to an empty string).
    - `client_id` (str, optional): OAuth2 client ID (default to an empty string).
    - `client_secret` (str, optional): OAuth2 client secret (default to an empty string).
    - `grant_type` (str, optional): OAuth2 grant type (default to "password").
    """

    username: str = Field(..., alias="email")
    password: str
    scope: str = ""
    client_id: str = ""
    client_secret: str = ""
    grant_type: str = "password"

class UserBase(BaseModel):
    """
    Base User schema.

    Attributes:
    - `id` (int): User ID.
    - `email` (str): User's email.
    - `is_active` (bool): User's active status.
    - `avatar_url` (str, optional): User's avatar URL (default to None).
    """

    id: int
    email: str
    is_active: bool
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    """
    User Creation schema (inherits from UserBase).

    Additional Attribute:
    - `password` (str): User's password.
    """

    password: str

class UserResponse(BaseModel):
    """
    User Response schema.

    Attributes:
    - `id` (int): User ID.
    - `email` (str): User's email.
    - `is_active` (bool): User's active status.
    """

    id: int
    email: str
    is_active: bool

class Contact(BaseModel):
    """
    Contact schema.

    Attributes:
    - `name` (str): Contact's name.
    - `email` (str): Contact's email.
    - `password` (str): Contact's password.
    """

    name: str
    email: str
    password: str  # Adjust the data type if necessary

class Token(BaseModel):
    """
    Token schema.

    Attributes:
    - `access_token` (str): Access token.
    - `token_type` (str): Token type.
    """

    access_token: str
    token_type: str

class Message(BaseModel):
    """
    Message schema.

    Attributes:
    - `message` (str): Message content.
    """

    message: str
