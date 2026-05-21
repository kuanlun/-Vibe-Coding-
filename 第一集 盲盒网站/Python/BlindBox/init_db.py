"""Database initialization module for Blind Box Display website."""
from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

import bcrypt


DB_PATH = Path(__file__).parent.parent.parent / "data" / "database.db"
SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS BlindBox (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL,
    image_path TEXT,
    is_secret INTEGER DEFAULT 0,
    created_at DATETIME,
    updated_at DATETIME
);

CREATE TABLE IF NOT EXISTS Admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    created_at DATETIME
);
"""


def get_connection() -> sqlite3.Connection:
    """Create a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = 1")
    return conn


def init_database() -> None:
    """Initialize the database with schema and default admin."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript(SCHEMA_SQL)

    cursor.execute(
        "SELECT id FROM Admin WHERE username = ?",
        ("admin",),
    )
    if cursor.fetchone() is None:
        password_hash = bcrypt.hashpw(
            "admin123".encode("utf-8"),
            bcrypt.gensalt(),
        ).decode("utf-8")
        cursor.execute(
            "INSERT INTO Admin (username, password, created_at) VALUES (?, ?, ?)",
            ("admin", password_hash, datetime.now().isoformat()),
        )

    conn.commit()
    conn.close()


def verify_admin(username: str, password: str) -> bool:
    """Verify admin credentials."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT password FROM Admin WHERE username = ?",
        (username,),
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return False
    stored_hash = row[0]
    return bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8"))


if __name__ == "__main__":
    init_database()
    print("Database initialized successfully.")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"Tables: {[t[0] for t in tables]}")

    cursor.execute("SELECT id, username, created_at FROM Admin")
    admins = cursor.fetchall()
    print(f"Admin records: {admins}")

    cursor.execute("SELECT password FROM Admin WHERE username = 'admin'")
    row = cursor.fetchone()
    if row:
        print(f"Password hash for admin: {row[0][:60]}...")
    conn.close()