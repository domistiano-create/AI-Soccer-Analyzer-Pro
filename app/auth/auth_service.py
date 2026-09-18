from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.auth.security import hash_password, verify_password, create_access_token
from app.database import get_db_connection

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/register")
def register_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """Registers a new user inside the permanent SQLite file and sets up a wallet."""
    username = form_data.username.strip()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if the user already exists in the file
    cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Securely hash the password string
    hashed = hash_password(form_data.password)
    
    # Save the user and instantly seed a free 10-credit starter wallet balance
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        cursor.execute("INSERT INTO wallets (username, balance) VALUES (?, 10.0)", (username,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        conn.close()
        raise HTTPException(status_code=500, detail="Database failure during user creation.")
        
    conn.close()
    return {"message": f"User {username} successfully registered with permanent storage!"}

@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """Queries the SQLite file to verify credentials and signs session tokens."""
    username = form_data.username.strip()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    
    if not row or not verify_password(form_data.password, row["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}
