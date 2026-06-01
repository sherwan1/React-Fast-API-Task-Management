"""Create database tables from models. Run: .venv/bin/python init_db.py"""

from databaseconfig import create_tables

if __name__ == "__main__":
    create_tables()
    print("Tables created (or already exist).")
