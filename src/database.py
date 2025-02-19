import sqlite3
import os
from contextlib import closing

DB_PATH = "data/jobs.db" 

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    if not os.path.exists("data"):
        os.makedirs("data") 

    with get_db_connection() as conn:
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

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS job_analysis (
                    job_id INTEGER PRIMARY KEY,
                    skills TEXT DEFAULT NULL,
                    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
                )
            """)
        conn.commit()
    print("SQLite init done")

def save_jobs(jobs):
    """ save jobs (avoid duplicate insertion)"""
    with sqlite3.connect(DB_PATH) as conn:
        with closing(conn.cursor()) as cursor:
            for job in jobs:
                try:
                    cursor.execute("""
                        INSERT OR IGNORE INTO jobs (
                            title, 
                            company, 
                            salary,
                            job_description, 
                            link
                        ) 
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        job[0],    # title
                        job[1],    # company
                        job[2],    # salary (使用 salaryLow)
                        job[3],    # job_description
                        job[4]     # link
                    ))
                except Exception as e:
                    print(f"Error saving job {job[0]}: {e}")
                    continue
        conn.commit()
    print(f" {len(jobs)} jobs saved")

def save_job_analysis(job_analysis):
    """ save job analysis (avoid duplicate insertion)"""
    with sqlite3.connect(DB_PATH) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.executemany("""
                INSERT OR IGNORE INTO job_analysis (job_id, skills)
                VALUES (?, ?)
            """, job_analysis)
        conn.commit()
    print(f" {len(job_analysis)} job analysis saved")

if __name__ == "__main__":
    init_db()