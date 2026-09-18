"""
auth_service.py

A simple in-memory "database" of users for now (a Python dict).
Later (Milestone 3) this gets replaced by a real database, but the
methods here — register() and login() — will stay the same shape.
That's the point of separating things into services: the storage
underneath can change without breaking the rest of the app.

Each registered user automatically gets their own Wallet, so money is
always tied to a real account from now on instead of a hardcoded ID.
"""

from app.users.user import User
from app.auth.security import hash_password, verify_password
from app.wallet.wallet import Wallet


class AuthService:
    def __init__(self):
        self.users_by_username = {}   # username -> User
        self.wallets_by_user_id = {}  # user.id -> Wallet

    def register(self, username: str, password: str) -> User:
        if username in self.users_by_username:
            raise ValueError(f"Username '{username}' is already taken")

        password_hash = hash_password(password)
        user = User(username=username, password_hash=password_hash)

        self.users_by_username[username] = user
        self.wallets_by_user_id[user.id] = Wallet(user_id=user.id)

        return user

    def login(self, username: str, password: str) -> User:
        user = self.users_by_username.get(username)

        if user is None:
            raise ValueError("Invalid username or password")

        if not verify_password(password, user.password_hash):
            raise ValueError("Invalid username or password")

        return user

    def get_wallet(self, user: User) -> Wallet:
        return self.wallets_by_user_id[user.id]
