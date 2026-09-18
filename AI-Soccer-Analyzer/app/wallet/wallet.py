"""
wallet.py

A Wallet keeps track of a user's money INSIDE the app.
In this simulation stage, nothing here touches real MTN MoMo, Airtel Money,
or card systems. It's just Python variables, so it's a safe place to learn
how balances, deposits, and spending should work before real money is involved.
"""


class Wallet:
    def __init__(self, user_id: str, starting_balance: float = 0.0):
        self.user_id = user_id
        self.balance = starting_balance          # money the user can use right now
        self.reserved = 0.0                       # money set aside (e.g. for a pending ticket)
        self.history = []                          # a simple log of everything that happened

    def deposit(self, amount: float, reference: str):
        """Add money to the wallet. Only ever called AFTER a payment is verified."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")

        self.balance += amount
        self.history.append({
            "type": "DEPOSIT",
            "amount": amount,
            "reference": reference,
            "balance_after": self.balance,
        })

    def reserve(self, amount: float, reference: str):
        """Set aside money for something like a ticket stake, without removing it yet."""
        if amount <= 0:
            raise ValueError("Reserve amount must be positive")

        if amount > self.balance:
            raise ValueError("Not enough available balance to reserve this amount")

        self.balance -= amount
        self.reserved += amount
        self.history.append({
            "type": "RESERVE",
            "amount": amount,
            "reference": reference,
            "balance_after": self.balance,
        })

    def release_reserve(self, amount: float, reference: str):
        """Give reserved money back to the available balance (e.g. a cancelled ticket)."""
        if amount <= 0:
            raise ValueError("Release amount must be positive")

        if amount > self.reserved:
            raise ValueError("Cannot release more reserved money than is currently reserved")

        self.reserved -= amount
        self.balance += amount
        self.history.append({
            "type": "RELEASE_RESERVE",
            "amount": amount,
            "reference": reference,
            "balance_after": self.balance,
        })

    def get_available_balance(self) -> float:
        return self.balance

    def __repr__(self):
        return f"Wallet(user={self.user_id}, available={self.balance}, reserved={self.reserved})"
