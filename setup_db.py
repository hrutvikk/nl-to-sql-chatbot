# setup_db.py
# Runs once on startup to create the database if it doesn't exist yet.

import os
from database import load_data_to_db

def ensure_db_exists():
    if not os.path.exists("data/superstore.db"):
        print("Database not found — creating it now...")
        load_data_to_db()
    else:
        print("Database already exists — skipping setup.")