import sqlite3
from db.database import DB_FILE

def get_world_time():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT world_date, world_time, turn_count, notes FROM world_time WHERE id = 1")
    result = c.fetchone()
    conn.close()
    return result

def set_world_time(date_str, time_str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Check if row with id = 1 exists
    c.execute("SELECT id FROM world_time WHERE id = 1")
    if c.fetchone():
        c.execute("UPDATE world_time SET world_date = ?, world_time = ? WHERE id = 1", (date_str, time_str))
    else:
        c.execute("INSERT INTO world_time (id, world_date, world_time, turn_count, notes) VALUES (1, ?, ?, 0, '')", (date_str, time_str))

    conn.commit()
    conn.close()


def increment_turns(count):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE world_time SET turn_count = turn_count + ? WHERE id = 1", (count,))
    conn.commit()
    conn.close()
