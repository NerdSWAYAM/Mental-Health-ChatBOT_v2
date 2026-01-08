import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = 'users.db'

def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        print(f"Database {DB_NAME} initialized.")

def add_user(first_name, last_name, email, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        # Check if user exists
        c.execute('SELECT * FROM users WHERE email = ?', (email,))
        if c.fetchone():
            return False, "User already exists"
        
        hashed_password = generate_password_hash(password)
        c.execute('INSERT INTO users (first_name, last_name, email, password) VALUES (?, ?, ?, ?)',
                  (first_name, last_name, email, hashed_password))
        conn.commit()
        return True, "User created successfully"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def authenticate_user(email, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute('SELECT password FROM users WHERE email = ?', (email,))
        row = c.fetchone()
        if row and check_password_hash(row[0], password):
            return True, "Login successful"
        return False, "Invalid email or password"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()
