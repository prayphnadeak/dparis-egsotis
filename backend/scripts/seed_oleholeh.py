"""
Seed script: membaca dparis_oleholeh.xlsx → mengisi tabel souvenir_shops di MySQL
Jalankan dari folder backend/: python scripts/seed_oleholeh.py
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
from app.models.souvenir import SouvenirShop  # noqa
import app.db.base  # noqa

XLSX_PATH = os.path.join(os.path.dirname(__file__), "..", "dparis_oleholeh.xlsx")


def seed():
    xlsx_abs = os.path.abspath(XLSX_PATH)
    if not os.path.exists(xlsx_abs):
        print(f"❌ File tidak ditemukan: {xlsx_abs}")
        sys.exit(1)

    # Pastikan tabel ada
    Base.metadata.create_all(bind=engine)

    wb = openpyxl.load_workbook(xlsx_abs)
    ws = wb.active  # Sheet1 (NO | NAMA | LINK)

    db = SessionLocal()
    try:
        # Hapus data lama
        deleted = db.query(SouvenirShop).delete()
        db.commit()
        print(f"🗑️  Hapus {deleted} data oleh-oleh lama")

        inserted = 0
        for row in ws.iter_rows(min_row=2, values_only=True):
            if not row or row[0] is None:
                continue
            no   = int(row[0])
            name = str(row[1]).strip() if row[1] else ""
            link = str(row[2]).strip() if len(row) > 2 and row[2] else ""
            if not name:
                continue
            obj = SouvenirShop(
                id=no,
                name=name,
                maps_link=link or None,
                is_active=True,
            )
            db.add(obj)
            inserted += 1

        db.commit()
        print(f"✅ {inserted} data oleh-oleh berhasil disimpan ke MySQL (tabel: souvenir_shops)")
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
