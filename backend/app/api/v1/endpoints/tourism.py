"""Tourism endpoints."""
from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_admin
from app.models.user import User
from app.schemas.tourism import TourismCreate, TourismUpdate, TourismResponse
from app.services.tourism_service import TourismService

router = APIRouter()


@router.get("/", response_model=List[TourismResponse], summary="Daftar objek wisata")
def list_tourism(q: str = "", category: Optional[str] = None, skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    return TourismService(db).list(q, category, skip, limit)


@router.get("/{id}", response_model=TourismResponse, summary="Detail objek wisata")
def get_tourism(id: int, db: Session = Depends(get_db)):
    return TourismService(db).get_or_404(id)


@router.post("/{id}/hit", summary="Tambah hit view wisata")
def hit_tourism(id: int, db: Session = Depends(get_db)):
    from app.models.tourism import TourismObject
    obj = db.get(TourismObject, id)
    if obj is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Not found")
    obj.view_count = (obj.view_count or 1) + 1
    db.commit()
    db.refresh(obj)
    return {"view_count": obj.view_count}


@router.post("/", response_model=TourismResponse, status_code=201, summary="Tambah objek wisata (admin)")
def create_tourism(data: TourismCreate, db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    return TourismService(db).create(data)


@router.put("/{id}", response_model=TourismResponse, summary="Update objek wisata (admin)")
def update_tourism(id: int, data: TourismUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    return TourismService(db).update(id, data)


@router.delete("/{id}", status_code=204, summary="Hapus objek wisata (admin)")
def delete_tourism(id: int, db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    TourismService(db).delete(id)
