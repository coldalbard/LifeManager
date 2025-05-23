import sqlite3


def get_connection():
    return sqlite3.connect("tasks.db")


def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       title TEXT NOT NULL,
                       is_done INTEGER DEFAULT 0)""")
        conn.commit()

