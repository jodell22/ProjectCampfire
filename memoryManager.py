# memoryManager.py

import sqlite3
from datetime import datetime

DB_FILE = "data/campfire.db"

def connect():
    return sqlite3.connect(DB_FILE)

def addMemory(subject, text, tags=None, participants=None, importance=0.5, source="event", private=False):
    tags = tags or []
    participants = participants or []

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO memory (subject, text, tags, participants, date, importance, source, private)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        subject,
        text,
        ",".join(tags),
        ",".join(participants),
        datetime.now().isoformat(),
        importance,
        source,
        int(private)
    ))
    conn.commit()
    conn.close()
    print(f"✅ Memory added for {subject}")

def listMemories(subject=None):
    conn = connect()
    cursor = conn.cursor()
    if subject:
        cursor.execute("SELECT id, subject, text FROM memory WHERE subject = ? ORDER BY date DESC", (subject,))
    else:
        cursor.execute("SELECT id, subject, text FROM memory ORDER BY date DESC")
    results = cursor.fetchall()
    conn.close()
    return results

def reinforceMemory(memory_id, amount=0.1):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE memory
        SET importance = MIN(1.0, importance + ?)
        WHERE id = ?
    """, (amount, memory_id))
    conn.commit()
    conn.close()
    print(f"🔁 Memory {memory_id} reinforced")
