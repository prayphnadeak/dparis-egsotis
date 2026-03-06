"""
Seed script: membaca dparis_akomodasi.xlsx → mengisi tabel accommodations di MySQL
Jalankan dari folder backend/: python scripts/seed_akomodasi.py
"""
import os
import sys

# Tambahkan root backend ke sys.path agar bisa import app.*
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import openpyxl
except ImportError:
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "openpyxl"], check=True)
    import openpyxl

from app.db.session import engine, SessionLocal
from app.models.base import Base
from app.models.accommodation import Accommodation  # noqa
import app.db.base  # noqa

XLSX_PATH = os.path.join(os.path.dirname(__file__), "..", "dparis_akomodasi.xlsx")


def ada(val) -> bool:
    """Konversi 'Ada'/'Tidak Ada' ke boolean."""
    return str(val).strip().lower() == "ada" if val else False


def clean_phone(val) -> str:
    if val is None:
        return ""
    s = str(val).strip()
    if s.isdigit() and len(s) >= 9:
        return "0" + s if not s.startswith("0") else s
    return s


def seed():
    xlsx_abs = os.path.abspath(XLSX_PATH)
    if not os.path.exists(xlsx_abs):
        print(f"❌ File tidak ditemukan: {xlsx_abs}")
        sys.exit(1)

    # Pastikan tabel ada
    Base.metadata.create_all(bind=engine)

    wb = openpyxl.load_workbook(xlsx_abs)

    # Coba baca dari Sheet3 dulu (sesuai struktur lama), fallback ke sheet aktif
    if "Sheet3" in wb.sheetnames:
        ws = wb["Sheet3"]
    else:
        ws = wb.active

    db = SessionLocal()
    try:
        # Hapus data lama
        deleted = db.query(Accommodation).delete()
        db.commit()
        print(f"🗑️  Hapus {deleted} data akomodasi lama")

        inserted = 0
        for row in ws.iter_rows(min_row=2, values_only=True):
            if not row or row[0] is None:
                continue

            # Kolom: NO, NAMA, ALAMAT, TELEPON, JENIS, KAMAR, TMP_TIDUR,
            #         AIR_PANAS, TV_KABEL, FREE_WIFI, RESTORAN, KLM_RENANG,
            #         KEBUGARAN, RUANG_MEETING, LINK
            no          = int(row[0])
            name        = str(row[1]).strip() if row[1] else ""
            address     = str(row[2]).strip() if len(row) > 2 and row[2] else ""
            phone       = clean_phone(row[3]) if len(row) > 3 else ""
            category    = str(row[4]).strip() if len(row) > 4 and row[4] else ""
            rooms       = int(row[5]) if len(row) > 5 and row[5] else 0
            beds        = int(row[6]) if len(row) > 6 and row[6] else 0
            hot_water   = ada(row[7])  if len(row) > 7  else False
            tv_cable    = ada(row[8])  if len(row) > 8  else False
            free_wifi   = ada(row[9])  if len(row) > 9  else False
            restaurant  = ada(row[10]) if len(row) > 10 else False
            swimming    = ada(row[11]) if len(row) > 11 else False
            gym         = ada(row[12]) if len(row) > 12 else False
            meeting     = ada(row[13]) if len(row) > 13 else False
            link        = str(row[14]).strip() if len(row) > 14 and row[14] else ""

            if not name:
                continue

            obj = Accommodation(
                id=no,
                name=name,
                address=address or None,
                phone=phone or None,
                category=category or "Akomodasi",
                total_rooms=rooms,
                total_beds=beds,
                hot_water=hot_water,
                tv_cable=tv_cable,
                free_wifi=free_wifi,
                restaurant=restaurant,
                swimming_pool=swimming,
                gym=gym,
                meeting_room=meeting,
                maps_link=link or None,
                is_active=True,
            )
            db.add(obj)
            inserted += 1

        db.commit()
        print(f"✅ {inserted} data akomodasi berhasil disimpan ke MySQL (tabel: accommodations)")
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
