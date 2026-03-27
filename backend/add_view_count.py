"""
One-time migration: add view_count column (default 1) to the 5 data tables.
Run once from the backend/ directory:
    python add_view_count.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "dparis.db")

TABLES = [
    "tourism_objects",
    "culinary_places",
    "souvenir_shops",
    "accommodations",
    "transportations",
]

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    errors = []
    for table in TABLES:
        try:
            cur.execute(f"ALTER TABLE {table} ADD COLUMN view_count INTEGER NOT NULL DEFAULT 1")
            print(f"  ✓ {table}: view_count column added")
        except sqlite3.OperationalError as e:
            msg = str(e)
            if "duplicate column" in msg.lower():
                print(f"  - {table}: view_count already exists (skipped)")
            else:
                errors.append(f"{table}: {msg}")
                print(f"  ✗ {table}: {msg}")
    conn.commit()
    conn.close()
    if errors:
        print("\nSome errors occurred:", errors)
    else:
        print("\nMigration OK – all tables processed.")

if __name__ == "__main__":
    main()
