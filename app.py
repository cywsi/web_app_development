import os
import sqlite3
from flask import Flask
from app.routes.routes import main_bp

# 取得資料庫預設路徑 (從 db.py 也可引用，但這裡為了 init_db 方便直接宣告或引用都可以)
from app.models.db import DB_PATH

def create_app():
    # 初始化 Flask 應用程式，並指定 template 與 static 的正確位置
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    
    # 載入設定
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-dev-key-for-local')
    
    # 註冊 Blueprint 路由
    app.register_blueprint(main_bp)

    return app

def init_db():
    """初始化資料庫與資料表結構"""
    schema_path = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')
    # 確保 instance 資料夾存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    print(f"Loading schema from: {schema_path}")
    print(f"Initializing database at: {DB_PATH}")
    
    conn = sqlite3.connect(DB_PATH)
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("Database structure initialized successfully.")

app = create_app()

if __name__ == '__main__':
    # 一般僅在本地開發時執行，部署時會交給 gunicorn 或 waitress 負責
    app.run(debug=True, port=5000)
