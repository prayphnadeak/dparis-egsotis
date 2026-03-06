"""
Standalone FastAPI mini-server untuk data Akomodasi
Menggunakan SQLite langsung (tanpa SQLAlchemy ORM)

Jalankan: py api_akomodasi.py
Akses: http://localhost:8000/api/v1/accommodations/
"""
import sqlite3
import os
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

DB_PATH = os.path.join(os.path.dirname(__file__), "dparis_akomodasi.db")

app = FastAPI(
    title="D'PARIS – Akomodasi API",
    description="API data akomodasi Kota Pagar Alam dari dparis_akomodasi.xlsx",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def row_to_dict(row: sqlite3.Row) -> dict:
    d = dict(row)
    # Ubah integer boolean ke True/False untuk JSON
    for key in ("hot_water", "tv_cable", "free_wifi", "restaurant",
                "swimming_pool", "gym", "meeting_room"):
        d[key] = bool(d[key])
    return d


@app.get("/")
def health():
    return {"status": "ok", "db": os.path.abspath(DB_PATH)}


@app.get("/api/v1/accommodations/", summary="Daftar semua akomodasi")
def list_accommodations(q: Optional[str] = None, category: Optional[str] = None):
    """
    Kembalikan daftar akomodasi. Gunakan `q` untuk pencarian nama,
    `category` untuk filter jenis akomodasi.
    """
    if not os.path.exists(DB_PATH):
        raise HTTPException(
            status_code=503,
            detail="Database belum dibuat. Jalankan: py scripts/seed_akomodasi.py"
        )
    conn = get_conn()
    sql = "SELECT * FROM accommodations WHERE is_active = 1"
    params: list = []
    if q:
        sql += " AND name LIKE ?"
        params.append(f"%{q}%")
    if category:
        sql += " AND category = ?"
        params.append(category)
    sql += " ORDER BY id"
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]


@app.get("/api/v1/accommodations/{item_id}", summary="Detail satu akomodasi")
def get_accommodation(item_id: int):
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=503, detail="Database belum dibuat.")
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM accommodations WHERE id = ? AND is_active = 1", (item_id,)
    ).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail=f"Akomodasi ID={item_id} tidak ditemukan")
    return row_to_dict(row)


@app.get("/api/v1/accommodations/categories/", summary="Daftar kategori akomodasi")
def list_categories():
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=503, detail="Database belum dibuat.")
    conn = get_conn()
    rows = conn.execute(
        "SELECT DISTINCT category FROM accommodations WHERE is_active = 1 ORDER BY category"
    ).fetchall()
    conn.close()
    return [r["category"] for r in rows]



# ── Oleh-Oleh endpoints ────────────────────────────────────────────────────

@app.get("/api/v1/oleholeh/", summary="Daftar toko oleh-oleh")
def list_oleholeh(q: Optional[str] = None):
    """Kembalikan daftar toko oleh-oleh. Gunakan `q` untuk pencarian nama."""
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=503, detail="Database belum dibuat.")
    conn = get_conn()
    sql = "SELECT * FROM oleholeh_shops WHERE is_active = 1"
    params: list = []
    if q:
        sql += " AND name LIKE ?"
        params.append(f"%{q}%")
    sql += " ORDER BY id"
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/api/v1/oleholeh/{item_id}", summary="Detail satu toko oleh-oleh")
def get_oleholeh(item_id: int):
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=503, detail="Database belum dibuat.")
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM oleholeh_shops WHERE id = ? AND is_active = 1", (item_id,)
    ).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail=f"Toko oleh-oleh ID={item_id} tidak ditemukan")
    return dict(row)



# ── Kuliner endpoints ───────────────────────────────────────────────────────

@app.get("/api/v1/kuliner/", summary="Daftar tempat kuliner")
def list_kuliner(q: Optional[str] = None):
    """Kembalikan daftar tempat kuliner. Gunakan `q` untuk pencarian nama."""
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=503, detail="Database belum dibuat.")
    conn = get_conn()
    sql = "SELECT * FROM kuliner_places WHERE is_active = 1"
    params: list = []
    if q:
        sql += " AND name LIKE ?"
        params.append(f"%{q}%")
    sql += " ORDER BY id"
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/api/v1/kuliner/{item_id}", summary="Detail satu tempat kuliner")
def get_kuliner(item_id: int):
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=503, detail="Database belum dibuat.")
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM kuliner_places WHERE id = ? AND is_active = 1", (item_id,)
    ).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail=f"Kuliner ID={item_id} tidak ditemukan")
    return dict(row)



# ── Wisata endpoints ────────────────────────────────────────────────────────

@app.get("/api/v1/wisata/", summary="Daftar objek wisata")
def list_wisata(q: Optional[str] = None):
    """Kembalikan daftar objek wisata. Gunakan `q` untuk pencarian nama."""
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=503, detail="Database belum dibuat.")
    conn = get_conn()
    sql = "SELECT * FROM wisata_places WHERE is_active = 1"
    params: list = []
    if q:
        sql += " AND name LIKE ?"
        params.append(f"%{q}%")
    sql += " ORDER BY id"
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/api/v1/wisata/{item_id}", summary="Detail satu objek wisata")
def get_wisata(item_id: int):
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=503, detail="Database belum dibuat.")
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM wisata_places WHERE id = ? AND is_active = 1", (item_id,)
    ).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail=f"Wisata ID={item_id} tidak ditemukan")
    return dict(row)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_akomodasi:app", host="0.0.0.0", port=8001, reload=True)
