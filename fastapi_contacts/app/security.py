# fastapi_contacts/app/security.py

import hashlib

SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"

def get_password_hash(password: str) -> str:
    """
    Hash the provided password using SHA-256 algorithm.

    Parameters:
    - `password` (str): Plain-text password to be hashed.

    Returns:
    - `str`: Hashed password.
    """
    return hashlib.sha256(password.encode()).hexdigest()
