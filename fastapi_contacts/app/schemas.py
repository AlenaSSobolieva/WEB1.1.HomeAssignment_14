# fastapi_contacts/app/schemas.py

from pydantic import BaseModel, Field
from typing import List, Optional

class OAuth2PasswordRequestForm(BaseModel):
    username: str = Field(..., alias="email")
    password: str
    scope: str = ""
    client_id: str = ""
    client_secret: str = ""
    grant_type: str = "password"

class UserBase(BaseModel):
    id: int
    email: str
    is_active: bool
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool

class Contact(BaseModel):
    name: str
    email: str
    password: str  # Adjust the data type if necessary

class Token(BaseModel):
    access_token: str
    token_type: str

class Message(BaseModel):  # Add this class
    message: str
