import sqlite3
import os
from datetime import datetime

DB_FILE = "data/campfire.db"

# Ensure the data directory exists
os.makedirs("data", exist_ok=True)

def initialize_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Players table
    c.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        owner_id INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Player stats table
    c.execute("""
    CREATE TABLE IF NOT EXISTS player_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id INTEGER NOT NULL,
        key TEXT NOT NULL,
        value TEXT,
        FOREIGN KEY (player_id) REFERENCES players (id) ON DELETE CASCADE
    )
    """)

    # Memory table
    c.execute("""
    CREATE TABLE IF NOT EXISTS memory (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Database schema checked and updated at", DB_FILE)

# Run schema init if this is called directly
if __name__ == "__main__":
    initialize_db()
