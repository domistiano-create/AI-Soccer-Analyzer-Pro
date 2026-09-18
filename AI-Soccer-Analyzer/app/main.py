"""
main.py

Run this file to see the app so far:
1. A user registers an account (password is hashed, never stored raw)
2. They log in
3. Their own wallet (created automatically at registration) receives
   a SIMULATED deposit, moving through PENDING -> SUCCESS/FAILED -> credit.

Run it with:  python -m app.main   (from the AI-Soccer-Analyzer folder)
"""

from app.auth.auth_service import AuthService
from app.payments.payment_service import PaymentService


def main():
    auth = AuthService()

    # 1. Register a new user. In a real app this password would come from
    #    a signup form, never hardcoded like this.
    user = auth.register(username="alice", password="correct-horse-battery-staple")
    print("Registered:", user)

    # 2. Log in (this proves the login/verify flow works, separately
    #    from registration)
    logged_in_user = auth.login(username="alice", password="correct-horse-battery-staple")
    print("Logged in as:", logged_in_user)

    # 3. Get that user's own wallet (created automatically at registration)
    wallet = auth.get_wallet(logged_in_user)
    print("Starting wallet:", wallet)

    # 4. Create the payment service, connected to that wallet
    payments = PaymentService(wallet)

    # 5. User asks to deposit 5,000 RWF via MTN MoMo
    reference = payments.create_deposit(amount=5000, method="MTN_MOMO")
    print(f"\nDeposit created. Reference: {reference}")
    print("Transaction:", payments.transactions[reference])

    # 6. We check/verify the payment (simulated)
    status = payments.verify_payment(reference)
    print(f"\nVerification result: {status}")

    # 7. Only credit the wallet if it succeeded
    credited = payments.credit_wallet_if_verified(reference)
    if credited:
        print("Wallet credited successfully.")
    else:
        print("Payment failed or was not confirmed. Wallet NOT credited.")

    print("\nFinal wallet:", wallet)
    print("\nWallet history:")
    for entry in wallet.history:
        print(" ", entry)


if __name__ == "__main__":
    main()
