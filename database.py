import sqlite3
from datetime import datetime

DB_PATH = "poems.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS saved_poems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            rhyme_scheme TEXT,
            primary_theme TEXT,
            feedback_summary TEXT,
            updated_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_or_update_poem(title: str, content: str, rhyme_scheme: str, theme: str, feedback: str, poem_id: int = None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    if poem_id:
        c.execute("""
            UPDATE saved_poems
            SET title=?, content=?, rhyme_scheme=?, primary_theme=?, feedback_summary=?, updated_at=?
            WHERE id=?
        """, (title, content, rhyme_scheme, theme, feedback, now, poem_id))
    else:
        c.execute("""
            INSERT INTO saved_poems (title, content, rhyme_scheme, primary_theme, feedback_summary, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, content, rhyme_scheme, theme, feedback, now))
    conn.commit()
    conn.close()

def get_all_poems():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM saved_poems ORDER BY updated_at DESC")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def delete_poem(poem_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM saved_poems WHERE id=?", (poem_id,))
    conn.commit()
    conn.close()