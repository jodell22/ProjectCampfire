# updatedb.py — safely applies updates to the Nova database
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import database

def run_updates():
    print("🔄 Running database update...")
    database.initialize_db()  # Ensures schema is up to date
    # Future update logic can go here
    print("✅ Update complete.")

if __name__ == "__main__":
    run_updates()
