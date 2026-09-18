"""
security.py

Handles password hashing. We NEVER store a user's real password anywhere —
only a scrambled ("hashed") version that can be checked but not reversed.

This uses Python's built-in hashlib with a per-password "salt" (random data
mixed in) so that even two users with the same password get different
hashes. This is a solid beginner-friendly approach using only the
standard library. (Production systems often use a dedicated library like
bcrypt or argon2 — worth upgrading to later, noted in the README.)
"""

import hashlib
import os


def hash_password(plain_password: str) -> str:
    salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        plain_password.encode("utf-8"),
        salt,
        100_000,  # number of iterations - higher = slower to crack, slower to check
    )
    # store salt + hash together, separated by a colon, so we can verify later
    return salt.hex() + ":" + hashed.hex()


def verify_password(plain_password: str, stored_hash: str) -> bool:
    if not isinstance(plain_password, str) or not isinstance(stored_hash, str):
        return False

    if not plain_password or not stored_hash or ":" not in stored_hash:
        return False

    try:
        salt_hex, hash_hex = stored_hash.split(":", 1)
        if not salt_hex or not hash_hex:
            return False
        salt = bytes.fromhex(salt_hex)
    except ValueError:
        return False

    new_hash = hashlib.pbkdf2_hmac(
        "sha256",
        plain_password.encode("utf-8"),
        salt,
        100_000,
    )
    return new_hash.hex() == hash_hex
