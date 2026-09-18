# AI Soccer Analyzer (Simulation Stage)

Built step by step, milestone by milestone. No real payment provider is
connected yet — this is for learning and building safely.

## How to run

1. Make sure you have Python 3 installed.
2. From this folder, run:

   python -m app.main

You should see: a user register, log in, and then a simulated MTN MoMo
deposit go through PENDING -> SUCCESS/FAILED and (usually) credit their
wallet.

To see the "wrong password" failure path specifically:

   python -m app.tests.test_auth

## What's here so far

- app/wallet/wallet.py             -> tracks a user's balance
- app/payments/payment_service.py  -> simulates deposit + verification
- app/users/user.py                -> a user's identity (id, username, password hash)
- app/auth/security.py             -> password hashing (never stores raw passwords)
- app/auth/auth_service.py         -> register() and login(), gives each user their own wallet
- app/main.py                      -> a runnable demo tying it all together
- app/tests/test_auth.py           -> shows the login failure path

## Notes for later

- Passwords are hashed with Python's built-in hashlib (PBKDF2 + a random
  salt per user). This is solid for learning; before any real production
  use, consider upgrading to a dedicated library like bcrypt or argon2.
- Users currently live in memory (a Python dict) and disappear when the
  program stops. Milestone 3 replaces this with a real database.

## What's next (Milestone 3)

Database: giving users, wallets, and transactions permanent storage
instead of living only in memory while the program runs.
