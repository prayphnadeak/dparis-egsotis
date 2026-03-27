"""
Seed script: membaca dparis_wisata.xlsx -> mengisi tabel tourism_objects di SQLite
Jalankan dari folder backend/: python scripts/seed_wisata.py

Kolom Excel: No(0), Nama(1), Link(2),
  Jarak ke GUNUNG DEMPO(3), Jarak ke PASAR DEMPO PERMAI(4),
  Jarak ke BANDARA ATUNG BUNGSU(5), Jarak ke RSUD BESEMAH(6),
  Jarak ke SPBU AIR PERIKAN(7), Jarak ke SPBU SIMPANG MANNA(8),
  Jarak ke SPBU PENGANDONAN(9), Jarak ke SPBU KARANG DALO(10)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import openpyxl
except ImportError:
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "openpyxl"], check=True)
    import openpyxl

from app.db.session import engine, SessionLocal
from app.models.base import Base
from app.models.tourism import TourismObject  # noqa
import app.db.base  # noqa

XLSX_PATH = os.path.join(os.path.dirname(__file__), "..", "dparis_wisata.xlsx")


def to_float(val):
    if val is None:
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None


def seed():
    xlsx_abs = os.path.abspath(XLSX_PATH)
    if not os.path.exists(xlsx_abs):
        print(f"[ERROR] File tidak ditemukan: {xlsx_abs}")
        sys.exit(1)

    Base.metadata.create_all(bind=engine)

    wb = openpyxl.load_workbook(xlsx_abs)
    ws = wb.active

    db = SessionLocal()
    try:
        deleted = db.query(TourismObject).delete()
        db.commit()
        print(f"[INFO] Hapus {deleted} data wisata lama")

        inserted = 0
        for row in ws.iter_rows(min_row=2, values_only=True):
            if not row or row[0] is None:
                continue

            def g(idx, default=None):
                return row[idx] if len(row) > idx else default

            no   = int(g(0, 0))
            name = str(g(1, "")).strip()
            rating = to_float(g(2))
            dt = str(g(3, "")).strip() if g(3) else None
            w_alam = str(g(4, "")).strip().lower() == "ya"
            w_budaya = str(g(5, "")).strip().lower() == "ya"
            w_buatan = str(g(6, "")).strip().lower() == "ya"
            link = str(g(7, "")).strip() if g(7) else ""

            dist_gunung_dempo         = to_float(g(8))
            dist_pasar_dempo_permai   = to_float(g(9))
            dist_bandara_atung_bungsu = to_float(g(10))
            dist_rsud_besemah         = to_float(g(11))
            dist_spbu_air_perikan     = to_float(g(12))
            dist_spbu_simpang_manna   = to_float(g(13))
            dist_spbu_pengandonan     = to_float(g(14))
            dist_spbu_karang_dalo     = to_float(g(15))

            if not name:
                continue

            obj = TourismObject(
                id=no,
                name=name,
                category="Wisata",
                rating=rating,
                daya_tarik=dt,
                maps_link=link or None,
                wisata_alam=w_alam,
                wisata_budaya=w_budaya,
                wisata_buatan=w_buatan,
                dist_gunung_dempo=dist_gunung_dempo,
                dist_pasar_dempo_permai=dist_pasar_dempo_permai,
                dist_bandara_atung_bungsu=dist_bandara_atung_bungsu,
                dist_rsud_besemah=dist_rsud_besemah,
                dist_spbu_air_perikan=dist_spbu_air_perikan,
                dist_spbu_simpang_manna=dist_spbu_simpang_manna,
                dist_spbu_pengandonan=dist_spbu_pengandonan,
                dist_spbu_karang_dalo=dist_spbu_karang_dalo,
                is_active=True,
            )
            db.add(obj)
            inserted += 1

        db.commit()
        print(f"[OK] {inserted} data wisata berhasil disimpan ke DB")
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
