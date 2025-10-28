import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "research_summaries.db")

def init_db():
    """Initialize the local SQLite DB"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            summary TEXT,
            link TEXT UNIQUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def store_summary(summary: str, link: str):
    """Stores a new summarized report (with link)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO summaries (summary, link) VALUES (?, ?)", (summary, link))
        conn.commit()
    except sqlite3.IntegrityError:
        # Skip if the same link already exists (deduplication)
        print(f"⚠️ Skipping duplicate link: {link}")
    conn.close()

def is_article_new(link: str) -> bool:
    """Check if the article link already exists in DB"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM summaries WHERE link = ?", (link,))
    exists = cursor.fetchone()
    conn.close()
    return not bool(exists)

def get_all_summaries():
    """Fetch all summaries"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT summary, link, created_at FROM summaries ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [{"summary": r[0], "link": r[1], "created_at": r[2]} for r in rows]

# Initialize DB at import time
init_db()
