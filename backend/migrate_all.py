"""
Migration: Tambah kolom rating dan distance ke 3 tabel (tourism_objects, culinary_places, souvenir_shops).
Jalankan dari backend/: python migrate_all.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.session import engine
from app.models.base import Base
from app.models.tourism import TourismObject  # noqa
from app.models.culinary import CulinaryPlace  # noqa
from app.models.souvenir import SouvenirShop  # noqa
import app.db.base  # noqa
from sqlalchemy import text
import subprocess

TABLES = {
    "tourism_objects": ["rating", "dist_gunung_dempo", "dist_pasar_dempo_permai",
                        "dist_bandara_atung_bungsu", "dist_rsud_besemah",
                        "dist_spbu_air_perikan", "dist_spbu_simpang_manna",
                        "dist_spbu_pengandonan", "dist_spbu_karang_dalo"],
    "culinary_places": ["rating", "dist_gunung_dempo", "dist_pasar_dempo_permai",
                        "dist_bandara_atung_bungsu", "dist_rsud_besemah",
                        "dist_spbu_air_perikan", "dist_spbu_simpang_manna",
                        "dist_spbu_pengandonan", "dist_spbu_karang_dalo"],
    "souvenir_shops":  ["rating", "dist_gunung_dempo", "dist_pasar_dempo_permai",
                        "dist_bandara_atung_bungsu", "dist_rsud_besemah",
                        "dist_spbu_air_perikan", "dist_spbu_simpang_manna",
                        "dist_spbu_pengandonan", "dist_spbu_karang_dalo"],
}

def migrate():
    with engine.connect() as conn:
        for table, cols in TABLES.items():
            result = conn.execute(text(f"PRAGMA table_info({table})"))
            existing = {row[1] for row in result.fetchall()}
            added = 0
            for col in cols:
                if col not in existing:
                    conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {col} REAL"))
                    added += 1
            conn.commit()
            print(f"[{table}] {added} kolom baru ditambahkan")

def reseed(script):
    result = subprocess.run(
        [sys.executable, script],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print("STDERR:", result.stderr)
        print(f"[ERROR] Reseed {script} gagal!")

if __name__ == "__main__":
    print("=== MIGRATION ===")
    migrate()
    print("\n=== RESEED WISATA ===")
    reseed("scripts/seed_wisata.py")
    print("\n=== RESEED KULINER ===")
    reseed("scripts/seed_kuliner.py")
    print("\n=== RESEED OLEHOLEH ===")
    reseed("scripts/seed_oleholeh.py")
    print("\n[DONE] Selesai!")
