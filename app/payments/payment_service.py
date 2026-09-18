import stripe
from fastapi import APIRouter, HTTPException, Request, Header, status
from fastapi.responses import RedirectResponse
from app.database import get_db_connection

router = APIRouter(prefix="/payments", tags=["Stripe Production Payments"])

# Set up your Stripe secret credentials configuration
# Sign up for a free developer account at https://stripe.com to fetch your API keys
stripe.api_key = "sk_test_your_secret_stripe_key_placeholder"
STRIPE_WEBHOOK_SECRET = "whsec_your_webhook_signing_secret_placeholder"

# Base URL pointing to your application workspace path
BASE_URL = "http://127.0.0.1:8000"

@router.post("/create-checkout-session")
def create_checkout_session(username: str, amount: float):
    """
    Constructs a secure Stripe hosted billing page session.
    Redirects user seamlessly to a safe credit card capture interface.
    """
    username = username.strip()
    if amount < 5.0:
        raise HTTPException(status_code=400, detail="Minimum deposit threshold is $5.00.")

    try:
        # Construct an isolated Stripe checkout session payload configuration
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f"AI Soccer Analyzer Wallet Top-Up ({amount} Credits)",
                        'description': f"Funding invoice profile allocation for user: {username}",
                    },
                    # Convert to cents integer format required by Stripe API core structures
                    'unit_amount': int(amount * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f"{BASE_URL}/?payment=success",
            cancel_url=f"{BASE_URL}/?payment=cancelled",
            # Pass user tracking variables securely inside meta blocks for asynchronous processing
            metadata={
                "username": username,
                "credit_amount": str(amount)
            }
        )
        return {"checkout_url": session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate transaction link: {str(e)}")

@router.post("/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    """
    Protected Stripe webhook endpoint.
    Intercepts global checkout confirmation logs asynchronously to fund user credit rows safely.
    """
    payload = await request.body()
    
    try:
        # Cryptographically parse and authenticate the transmission package signature
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid data payload package.")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Cryptographic signature verification failed.")

    # Process successful checkout completions securely
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Pull your application profile reference meta tags back out of the transaction object
        username = session.get('metadata', {}).get('username')
        credit_amount = float(session.get('metadata', {}).get('credit_amount', 0))
        
        if username:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Fetch current row metrics from persistent SQLite storage file
            cursor.execute("SELECT balance FROM wallets WHERE username = ?", (username,))
            row = cursor.fetchone()
            
            if row:
                new_balance = row["balance"] + credit_amount
                cursor.execute("UPDATE wallets SET balance = ? WHERE username = ?", (new_balance, username))
                conn.commit()
                print(f"💰 STRIPE SUCCESS: Injected +{credit_amount} credits into permanent row for user '{username}'. New balance: {new_balance}")
            
            conn.close()
            
    return {"status": "success"}
