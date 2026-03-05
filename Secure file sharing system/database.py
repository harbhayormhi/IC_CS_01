import sqlite3

def init_db():
    conn = sqlite3.connect("instance/database.db")
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            public_key TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            owner_id INTEGER,
            encrypted_key BLOB
        )
    ''')

    conn.commit()
    conn.close()
