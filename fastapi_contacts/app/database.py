# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://postgres:Queen2001)@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Function to get a database session.

    Usage:
    ```
    with get_db() as db:
        # Perform database operations
    ```

    :return: Database session.
    """
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


def create_tables():
    """
    Function to create database tables.

    Usage:
    ```
    create_tables()
    ```

    This function should be called to create tables before running the application.
    """
    Base.metadata.create_all(bind=engine)
