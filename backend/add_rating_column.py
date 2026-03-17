"""
Migration + Reseed: Tambah kolom rating dan distance ke tabel accommodations.
Jalankan dari folder backend/: python add_rating_column.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.session import engine
from app.models.base import Base
from app.models.accommodation import Accommodation  # noqa
import app.db.base  # noqa
from sqlalchemy import text

def migrate():
    """Add new columns to accommodations table if they don't exist."""
    new_columns = [
        ("rating",                    "REAL"),
        ("dist_gunung_dempo",         "REAL"),
        ("dist_pasar_dempo_permai",   "REAL"),
        ("dist_bandara_atung_bungsu", "REAL"),
        ("dist_rsud_besemah",         "REAL"),
        ("dist_spbu_air_perikan",     "REAL"),
        ("dist_spbu_simpang_manna",   "REAL"),
        ("dist_spbu_pengandonan",     "REAL"),
        ("dist_spbu_karang_dalo",     "REAL"),
    ]

    with engine.connect() as conn:
        # Get existing columns
        result = conn.execute(text("PRAGMA table_info(accommodations)"))
        existing = {row[1] for row in result.fetchall()}
        print(f"[INFO] Kolom yang sudah ada: {len(existing)} kolom")

        for col_name, col_type in new_columns:
            if col_name not in existing:
                conn.execute(text(f"ALTER TABLE accommodations ADD COLUMN {col_name} {col_type}"))
                print(f"  [+] Ditambahkan kolom: {col_name}")
            else:
                print(f"  [=] Kolom sudah ada: {col_name}")
        conn.commit()

    print("[OK] Migration selesai.\n")


def reseed():
    """Re-seed accommodation data from Excel."""
    import subprocess
    result = subprocess.run(
        [sys.executable, "scripts/seed_akomodasi.py"],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    if result.returncode != 0:
        print("[ERROR] Reseed gagal!")
        sys.exit(1)


if __name__ == "__main__":
    print("=== MIGRATION: Tambah kolom rating & jarak ke DB ===")
    migrate()
    print("=== RESEED: Import ulang data dari Excel ===")
    reseed()
    print("\n[DONE] Selesai! DB sudah diperbarui dengan data rating dan jarak landmark.")
