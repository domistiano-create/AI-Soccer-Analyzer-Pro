from fastapi import APIRouter, HTTPException, status
from app.database import get_db_connection

router = APIRouter(prefix="/wallet", tags=["Wallet System"])

@router.get("/balance")
def get_balance(username: str):
    """Fetches a user's wallet credit balance straight from the storage file."""
    username = username.strip()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT balance FROM wallets WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User wallet profile not found. Please register first."
        )
        
    return {"username": username, "balance": row["balance"]}

@router.post("/add-credits")
def add_credits(username: str, amount: float):
    """Modifies the saved file database row increasing a user's coins balance."""
    username = username.strip()
    if amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Deposit amount must be greater than zero."
        )
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT balance FROM wallets WHERE username = ?", (username,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="User wallet entry not found.")
        
    new_balance = row["balance"] + amount
    cursor.execute("UPDATE wallets SET balance = ? WHERE username = ?", (new_balance, username))
    conn.commit()
    conn.close()
    
    return {"message": f"Successfully added {amount} credits.", "new_balance": new_balance}
