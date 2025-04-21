import sqlite3
from pathlib import Path

DB_FILE = Path("./data/campfire.db")  # ← Update this with your actual DB path

conn = sqlite3.connect(DB_FILE)
c = conn.cursor()

# Check what's currently in the DB
c.execute("ALTER TABLE world_time RENAME COLUMN current_time TO world_time;")
rows = c.fetchall()

for row in rows:
    print(row)

conn.close()
