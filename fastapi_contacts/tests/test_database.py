# tests/test_database.py

import unittest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from fastapi_contacts.app.database import create_tables, get_db, Base

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class TestDatabase(unittest.TestCase):

    def test_create_tables(self):
        # Create tables in a temporary SQLite database
        create_tables()

        # Check if the tables exist
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        # Assuming you have models named User and Contact
        expected_tables = ["users", "contacts"]  # Corrected table names
        for table in expected_tables:
            self.assertIn(table, tables)

    def test_get_db(self):
        # Test the get_db function
        with get_db() as db:
            self.assertIsNotNone(db)
            # You can add more assertions or database operations here

if __name__ == '__main__':
    unittest.main()