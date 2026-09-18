"""
payment_service.py

This is a SIMULATED payment service. It mimics the shape of a real one
(create -> verify -> record -> credit wallet) without ever contacting
MTN MoMo, Airtel Money, or a card gateway. This lets you build and test
the rest of the app before dealing with any real provider or real money.

Every real transaction in the actual design report has a state:
PENDING, SUCCESS, FAILED, CANCELLED, REFUNDED.
We reproduce that here so the rest of your app can be written the same
way now as it will work later.
"""

import uuid
import random


class PaymentService:
    def __init__(self, wallet):
        self.wallet = wallet
        self.transactions = {}   # reference -> transaction dict

    def create_deposit(self, amount: float, method: str) -> str:
        """
        Step 1: user asks to deposit money via a method
        (e.g. 'MTN_MOMO', 'AIRTEL_MONEY', 'CARD').
        Returns a transaction reference.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")

        if method not in ("MTN_MOMO", "AIRTEL_MONEY", "CARD"):
            raise ValueError(f"Unsupported method: {method}")

        reference = str(uuid.uuid4())[:8]
        self.transactions[reference] = {
            "reference": reference,
            "amount": amount,
            "method": method,
            "status": "PENDING",
            "credited": False,
        }
        return reference

    def verify_payment(self, reference: str) -> str:
        """
        Step 2: in real life, this checks with the provider or waits for a
        webhook callback. Here, we simulate a 90% success rate so you can
        see both the success and failure paths.
        """
        txn = self.transactions[reference]

        if txn["status"] != "PENDING":
            return txn["status"]

        txn["status"] = "SUCCESS" if random.random() < 0.9 else "FAILED"
        return txn["status"]

    def credit_wallet_if_verified(self, reference: str):
        """
        Step 3: only credit the wallet if the transaction actually succeeded.
        This mirrors the real rule: 'wallet balance is only updated after
        an authorized confirmation of the transaction.'
        """
        txn = self.transactions[reference]

        if txn["status"] == "SUCCESS" and not txn.get("credited", False):
            self.wallet.deposit(txn["amount"], reference=reference)
            txn["credited"] = True
            return True

        return False
