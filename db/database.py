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
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,
        text TEXT NOT NULL,
        tags TEXT,
        participants TEXT,
        date TEXT DEFAULT CURRENT_TIMESTAMP,
        importance REAL DEFAULT 0.5,
        source TEXT DEFAULT 'event',
        private BOOLEAN DEFAULT 0
    )
    """)

    c.execute('''
        CREATE TABLE IF NOT EXISTS world_time (
            id INTEGER PRIMARY KEY,
            current_date TEXT NOT NULL,
            current_time TEXT NOT NULL,
            turn_count INTEGER DEFAULT 0,
            notes TEXT
        )
    ''')

    c.execute("SELECT COUNT(*) FROM world_time")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO world_time (current_date, current_time, turn_count, notes) VALUES (?, ?, ?, ?)",
                  ("1 Stormtide 843", "08:00 AM", 0, ""))

    conn.commit()
    conn.close()
    print("✅ Database schema checked and updated at", DB_FILE)

# Run schema init if this is called directly
if __name__ == "__main__":
    initialize_db()
