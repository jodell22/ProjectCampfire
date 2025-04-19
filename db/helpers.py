import sqlite3
from db.database import DB_FILE

# --- PLAYER HELPERS ---

def set_player_owner(name, owner_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE players SET owner_id = ? WHERE name = ?", (owner_id, name))
    conn.commit()
    conn.close()



def get_player_by_name(name):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM players WHERE name = ?", (name,))
    player = c.fetchone()
    conn.close()
    return player

def create_player(name, owner_id=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO players (name, owner_id) VALUES (?, ?)", (name, owner_id))
    conn.commit()
    conn.close()

def get_all_players():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT name FROM players")
    players = [row[0] for row in c.fetchall()]
    conn.close()
    return players

def delete_player_by_name(name):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM players WHERE name = ?", (name,))
    conn.commit()
    conn.close()

# --- STAT HELPERS ---

def set_player_stat(player_name, key, value):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id FROM players WHERE name = ?", (player_name,))
    player_id = c.fetchone()
    if not player_id:
        conn.close()
        return False

    player_id = player_id[0]
    # Try update first
    c.execute("UPDATE player_stats SET value = ? WHERE player_id = ? AND key = ?", (value, player_id, key))
    if c.rowcount == 0:
        # Insert if not exists
        c.execute("INSERT INTO player_stats (player_id, key, value) VALUES (?, ?, ?)", (player_id, key, value))

    conn.commit()
    conn.close()
    return True

def get_player_stats(player_name):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id FROM players WHERE name = ?", (player_name,))
    player_id = c.fetchone()
    if not player_id:
        conn.close()
        return None

    player_id = player_id[0]
    c.execute("SELECT key, value FROM player_stats WHERE player_id = ?", (player_id,))
    stats = dict(c.fetchall())
    conn.close()
    return stats

# --- MEMORY HELPERS ---

def set_memory(key, value):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("REPLACE INTO memory (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def get_memory(key):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT value FROM memory WHERE key = ?", (key,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def get_all_memory():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT key, value FROM memory")
    memory = dict(c.fetchall())
    conn.close()
    return memory

def delete_memory(key):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM memory WHERE key = ?", (key,))
    conn.commit()
    conn.close()

def clear_memory():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM memory")
    conn.commit()
    conn.close()
