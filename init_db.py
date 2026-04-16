import os
import sqlite3
from app.models.db import DB_PATH

def init_db():
    schema_path = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("Database structure initialized successfully.")

if __name__ == '__main__':
    init_db()
