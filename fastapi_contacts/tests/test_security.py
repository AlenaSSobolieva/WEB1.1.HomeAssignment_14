# fastapi_contacts/tests/test_security.py

import unittest
import hashlib  # Add this line to import hashlib
from fastapi_contacts.app.security import get_password_hash, SECRET_KEY, ALGORITHM

class TestSecurity(unittest.TestCase):

    def test_get_password_hash(self):
        plain_text_password = "test_password"
        hashed_password = get_password_hash(plain_text_password)

        # Ensure that the hashed password is not equal to the plain text password
        self.assertNotEqual(hashed_password, plain_text_password)

        # Manually hash the plain text password using hashlib.sha256 for comparison
        expected_hash = hashlib.sha256(plain_text_password.encode()).hexdigest()
        self.assertEqual(hashed_password, expected_hash)

    def test_secret_key(self):
        # Ensure that the secret key is defined and is not an empty string
        self.assertIsNotNone(SECRET_KEY)
        self.assertNotEqual(SECRET_KEY, "")

    def test_algorithm(self):
        # Ensure that the algorithm is defined and is not an empty string
        self.assertIsNotNone(ALGORITHM)
        self.assertNotEqual(ALGORITHM, "")

if __name__ == '__main__':
    unittest.main()
