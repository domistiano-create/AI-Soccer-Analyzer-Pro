"""
test_auth.py

A very simple, beginner-friendly test (not using a testing framework yet)
that shows what happens when someone logs in with the WRONG password.
Run it with:  python -m app.tests.test_auth
"""

from app.auth.auth_service import AuthService


def main():
    auth = AuthService()
    auth.register(username="bob", password="my-real-password")

    try:
        auth.login(username="bob", password="wrong-password")
        print("This should not print - login should have failed!")
    except ValueError as e:
        print("Got the expected error:", e)

    # Now show that the correct password still works
    user = auth.login(username="bob", password="my-real-password")
    print("Correct password worked:", user)


if __name__ == "__main__":
    main()
