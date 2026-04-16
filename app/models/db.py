import sqlite3
import os

# 定義資料庫路徑：專案根目錄/instance/database.db
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """取得 SQLite 資料庫連線"""
    # 確保資料夾存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    # 讓 SELECT 回傳的資料可以用 key 存取 (例如 row['id'])
    conn.row_factory = sqlite3.Row
    return conn
