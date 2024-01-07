# app/security.py

SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"

# Add the function to hash passwords
import hashlib

def get_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()
