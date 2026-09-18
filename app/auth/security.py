import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from jose import jwt

# Secret keys for signing authentication tokens
SECRET_KEY = "your-super-secret-soccer-key"
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    """Converts a plain text password into a secure hash using hashlib."""
    # Generate a secure random salt to protect the password
    salt = secrets.token_hex(16)
    # Combine password and salt, then hash using SHA-256
    hash_object = hashlib.sha256((password + salt).encode())
    hashed_password = hash_object.hexdigest()
    # Store both the salt and the hash together split by a colon
    return f"{salt}:{hashed_password}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Checks if a typed password matches the saved hash and salt."""
    try:
        salt, stored_hash = hashed_password.split(":")
        hash_object = hashlib.sha256((plain_password + salt).encode())
        return hash_object.hexdigest() == stored_hash
    except ValueError:
        return False

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Generates a secure JWT token for user login sessions."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
