# fastapi_contacts/app/crud.py

from sqlalchemy.orm import Session
from fastapi_contacts.app.models import User, UserCreate, Contact
from passlib.context import CryptContext
from fastapi_contacts.app.security import get_password_hash


crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user: UserCreate):
    """
    Create a new user in the database.

    :param db: Database session.
    :param user: UserCreate instance containing user details.
    :return: Created user.
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    """
    Retrieve a user from the database by email.

    :param db: Database session.
    :param email: Email of the user to retrieve.
    :return: User information.
    """
    return db.query(User).filter(User.email == email).first()

def create_contact(db: Session, contact: Contact):
    """
    Create a new contact in the database.

    :param db: Database session.
    :param contact: Contact instance containing contact details.
    :return: Created contact.
    """
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_contact_by_email(db: Session, email: str):
    """
    Retrieve a contact from the database by email.

    :param db: Database session.
    :param email: Email of the contact to retrieve.
    :return: Contact information.
    """
    return db.query(Contact).filter(Contact.email == email).first()
