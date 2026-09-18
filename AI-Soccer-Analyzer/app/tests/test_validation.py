import unittest

from app.auth.security import verify_password
from app.payments.payment_service import PaymentService
from app.wallet.wallet import Wallet


class ValidationTests(unittest.TestCase):
    def test_verify_password_rejects_malformed_hash(self):
        self.assertFalse(verify_password("secret", "bad-hash"))

    def test_create_deposit_rejects_non_positive_amount(self):
        service = PaymentService(Wallet("user-1"))

        with self.assertRaisesRegex(ValueError, "positive"):
            service.create_deposit(amount=0, method="MTN_MOMO")

    def test_credit_wallet_if_verified_only_applies_once(self):
        wallet = Wallet("user-2")
        service = PaymentService(wallet)
        ref = service.create_deposit(amount=100, method="MTN_MOMO")
        service.transactions[ref]["status"] = "SUCCESS"

        self.assertTrue(service.credit_wallet_if_verified(ref))
        self.assertEqual(wallet.balance, 100.0)
        self.assertFalse(service.credit_wallet_if_verified(ref))
        self.assertEqual(wallet.balance, 100.0)


if __name__ == "__main__":
    unittest.main()
