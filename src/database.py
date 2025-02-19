import sqlite3
import os
from contextlib import closing

DB_PATH = "data/jobs.db" 

def init_db():
    if not os.path.exists("data"):
        os.makedirs("data") 

    with sqlite3.connect(DB_PATH) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    company TEXT NOT NULL,
                    salary TEXT DEFAULT 'not provided',
                    job_description TEXT,
                    link TEXT UNIQUE,
                    is_applied BOOLEAN DEFAULT FALSE,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
        conn.commit()
    print("SQLite init done")

def get_db_connection():
    """ 取得 SQLite 資料庫連線 """
    return sqlite3.connect(DB_PATH)

if __name__ == "__main__":
    init_db()