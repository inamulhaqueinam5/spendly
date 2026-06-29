"""SQLite data layer for Spendly (Step 1 — Database Setup)."""

import os
import sqlite3
from datetime import datetime

from werkzeug.security import generate_password_hash

# Absolute path to spendly.db in the project root, independent of the CWD.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, "spendly.db")

# Fixed category list (spec §10).
CATEGORIES = ["Food", "Transport", "Bills", "Health", "Entertainment", "Shopping", "Other"]


def get_db():
    """Return a SQLite connection with dict-like rows and foreign keys enforced."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create the users and expenses tables if they don't already exist."""
    conn = get_db()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                name          TEXT NOT NULL,
                email         TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at    TEXT DEFAULT (datetime('now'))
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL REFERENCES users(id),
                amount      REAL NOT NULL,
                category    TEXT NOT NULL,
                date        TEXT NOT NULL,
                description TEXT,
                created_at  TEXT DEFAULT (datetime('now'))
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def seed_db():
    """Insert one demo user and 8 sample expenses — only once (idempotent)."""
    conn = get_db()
    try:
        existing = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if existing > 0:
            return

        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
        )
        user_id = cursor.lastrowid

        # Dates spread across the current month, always valid (days 1..28).
        now = datetime.now()

        def day(d):
            return f"{now.year:04d}-{now.month:02d}-{d:02d}"

        # 8 expenses: every category at least once, plus a second Food entry.
        expenses = [
            (user_id, 12.50, "Food", day(2), "Lunch at cafe"),
            (user_id, 30.00, "Transport", day(4), "Monthly metro top-up"),
            (user_id, 85.75, "Bills", day(6), "Electricity bill"),
            (user_id, 45.00, "Health", day(9), "Pharmacy"),
            (user_id, 18.99, "Entertainment", day(12), "Movie ticket"),
            (user_id, 64.20, "Shopping", day(15), "New shoes"),
            (user_id, 9.99, "Other", day(18), "Misc subscription"),
            (user_id, 22.40, "Food", day(21), "Groceries"),
        ]
        conn.executemany(
            "INSERT INTO expenses (user_id, amount, category, date, description) "
            "VALUES (?, ?, ?, ?, ?)",
            expenses,
        )
        conn.commit()
    finally:
        conn.close()
