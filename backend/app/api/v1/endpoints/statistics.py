"""Statistics tracking endpoints."""
from datetime import date
from typing import Dict, Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.dependencies import get_db
from app.models.user_log import UserLog

router = APIRouter()

BASE_VISITORS = 238
BASE_DOWNLOADERS = 30

@router.get("/total", response_model=Dict[str, int], summary="Dapatkan total pengunjung & pengunduh")
def get_total_statistics(db: Session = Depends(get_db)):
    result = db.query(
        func.sum(UserLog.visitor_count).label("total_visitors"),
        func.sum(UserLog.downloader_count).label("total_downloaders")
    ).first()
    
    db_visitors = result.total_visitors or 0
    db_downloaders = result.total_downloaders or 0
    
    return {
        "visitor_total": BASE_VISITORS + db_visitors,
        "downloader_total": BASE_DOWNLOADERS + db_downloaders
    }

@router.get("/dashboard_counts", response_model=Dict[str, Any], summary="Dapatkan hitungan direktori mentah database")
def get_dashboard_counts(db: Session = Depends(get_db)):
    from app.models.tourism import TourismObject
    from app.models.accommodation import Accommodation
    from app.models.culinary import CulinaryPlace
    from app.models.souvenir import SouvenirShop
    from app.models.transportation import Transportation

    # Wisata
    wisata_raw = db.query(TourismObject.category, func.count(TourismObject.id)).group_by(TourismObject.category).all()
    wisata_cats = {row[0] or "Tanpa Kategori": row[1] for row in wisata_raw}
    wisata_total = sum(wisata_cats.values())
    
    wisata_dt_raw = db.query(TourismObject.daya_tarik, func.count(TourismObject.id)).group_by(TourismObject.daya_tarik).all()
    wisata_dt_cats = {row[0] or "Tanpa Keterangan": row[1] for row in wisata_dt_raw}

    # Akomodasi
    akomodasi_raw = db.query(Accommodation.category, func.count(Accommodation.id)).group_by(Accommodation.category).all()
    akomodasi_cats = {row[0] or "Tanpa Kategori": row[1] for row in akomodasi_raw}
    akomodasi_total = sum(akomodasi_cats.values())

    # Kuliner
    kuliner_raw = db.query(CulinaryPlace.category, func.count(CulinaryPlace.id)).group_by(CulinaryPlace.category).all()
    kuliner_cats = {row[0] or "Tanpa Kategori": row[1] for row in kuliner_raw}
    kuliner_total = sum(kuliner_cats.values())

    # Oleh-oleh (No category column)
    oleh_total = db.query(func.count(SouvenirShop.id)).scalar() or 0
    oleh_cats = {"Semua": oleh_total} if oleh_total > 0 else {}

    # Transportasi (Moda Transportasi)
    transport_raw = db.query(Transportation.category, func.count(Transportation.id)).group_by(Transportation.category).all()
    transport_cats = {row[0] or "Lainnya": row[1] for row in transport_raw}
    transport_total = sum(transport_cats.values())

    return {
        "wisata": {
            "total": wisata_total, 
            "categories": wisata_cats,
            "daya_tarik": wisata_dt_cats
        },
        "akomodasi": {"total": akomodasi_total, "categories": akomodasi_cats},
        "kuliner": {"total": kuliner_total, "categories": kuliner_cats},
        "oleholeh": {"total": oleh_total, "categories": oleh_cats},
        "transportasi": {"total": transport_total, "categories": transport_cats},
    }

@router.get("/daily", summary="Dapatkan log statistik pengunjung harian")
def get_daily_statistics(db: Session = Depends(get_db)):
    logs = db.query(UserLog).order_by(UserLog.date.asc()).all()
    
    return [
        {
            "date": log.date.strftime("%Y-%m-%d"),
            "visitor_count": log.visitor_count,
            "downloader_count": log.downloader_count
        }
        for log in logs
    ]

@router.post("/visit", summary="Catat kunjungan baru")
def log_visit(db: Session = Depends(get_db)):
    today = date.today()
    log = db.query(UserLog).filter(UserLog.date == today).first()
    if not log:
        log = UserLog(date=today, visitor_count=1, downloader_count=0)
        db.add(log)
    else:
        log.visitor_count += 1
    db.commit()
    return {"status": "ok"}

@router.post("/download", summary="Catat unduhan PWA baru")
def log_download(db: Session = Depends(get_db)):
    today = date.today()
    log = db.query(UserLog).filter(UserLog.date == today).first()
    if not log:
        log = UserLog(date=today, visitor_count=0, downloader_count=1)
        db.add(log)
    else:
        log.downloader_count += 1
    db.commit()
    return {"status": "ok"}
