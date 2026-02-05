import sqlite3
import hashlib
import os

# Create data directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Connection to users database
def connect_users():
    conn = sqlite3.connect('data/users.db')
    return conn

# Create users table
def create_users_table():
    conn = connect_users()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            creation_date TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

# Encrypt password
def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register new user
def register_user(username, password):
    try:
        conn = connect_users()
        cursor = conn.cursor()
        
        from datetime import datetime
        creation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        encrypted_password = encrypt_password(password)
        
        cursor.execute('''
            INSERT INTO users (username, password, creation_date)
            VALUES (?, ?, ?)
        ''', (username, encrypted_password, creation_date))
        
        conn.commit()
        conn.close()
        
        # Create specific database for the user
        create_user_database(username)
        
        return True, "User registered successfully!"
    except sqlite3.IntegrityError:
        return False, "This user already exists!"
    except Exception as e:
        return False, f"Registration error: {str(e)}"

# Verify login
def verify_login(username, password):
    try:
        conn = connect_users()
        cursor = conn.cursor()
        
        encrypted_password = encrypt_password(password)
        
        cursor.execute('''
            SELECT * FROM users 
            WHERE username = ? AND password = ?
        ''', (username, encrypted_password))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            # Ensure user's database exists
            database_name = f'data/{username}_finances.db'
            if not os.path.exists(database_name):
                create_user_database(username)
            
            return True, "Login successful!"
        else:
            return False, "Incorrect username or password!"
    except Exception as e:
        return False, f"Login error: {str(e)}"

# Check if user exists
def user_exists(username):
    try:
        conn = connect_users()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        conn.close()
        
        return result is not None
    except:
        return False

# Create specific database for a user
def create_user_database(username):
    """Creates a separate database for each user"""
    database_name = f'data/{username}_finances.db'
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    
    # Create categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    
    # Create revenues table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS revenues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            value REAL NOT NULL
        )
    ''')
    
    # Create expenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            value REAL NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

# Get user's database path
def get_user_database(username):
    """Returns the path to the user's database"""
    return f'data/{username}_finances.db'

# Initialize database
create_users_table()
