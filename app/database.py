import sqlite3
import os

DB_PATH = "soccer_analyzer.db"

def get_db_connection():
    """Opens a connection to the permanent SQLite database file."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name like dicts
    return conn

def init_db():
    """Creates the user accounts and wallet tracking tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Create the permanent users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    
    # 2. Create the permanent wallets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wallets (
            username TEXT PRIMARY KEY,
            balance REAL DEFAULT 10.0,
            FOREIGN KEY (username) REFERENCES users (username)
        )
    ''')
    
    conn.commit()
    conn.close()
