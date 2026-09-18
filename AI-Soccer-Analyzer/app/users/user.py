"""
user.py

A User is just an identity: who they are. It does NOT hold money logic
(that's the Wallet's job) and does NOT hold the password directly
(that's handled by auth/security.py) — keeping these separate means
a bug in one area can't accidentally leak into another.
"""

import uuid


class User:
    def __init__(self, username: str, password_hash: str):
        self.id = str(uuid.uuid4())[:8]
        self.username = username
        self.password_hash = password_hash   # never store the raw password!

    def __repr__(self):
        return f"User(id={self.id}, username={self.username})"
