"""Culinary endpoints."""
from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_admin
from app.models.user import User
from app.schemas.culinary import CulinaryCreate, CulinaryUpdate, CulinaryResponse
from app.services.culinary_service import CulinaryService

router = APIRouter()


@router.get("/", response_model=List[CulinaryResponse], summary="Daftar tempat kuliner")
def list_culinary(q: str = "", category: Optional[str] = None, skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    return CulinaryService(db).list(q, category, skip, limit)


@router.get("/{id}", response_model=CulinaryResponse, summary="Detail tempat kuliner")
def get_culinary(id: int, db: Session = Depends(get_db)):
    return CulinaryService(db).get_or_404(id)


@router.post("/{id}/hit", summary="Tambah hit view kuliner")
def hit_culinary(id: int, db: Session = Depends(get_db)):
    from app.models.culinary import CulinaryPlace
    obj = db.get(CulinaryPlace, id)
    if obj is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Not found")
    obj.view_count = (obj.view_count or 1) + 1
    db.commit()
    db.refresh(obj)
    return {"view_count": obj.view_count}


@router.post("/", response_model=CulinaryResponse, status_code=201, summary="Tambah kuliner (admin)")
def create_culinary(data: CulinaryCreate, db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    return CulinaryService(db).create(data)


@router.put("/{id}", response_model=CulinaryResponse, summary="Update kuliner (admin)")
def update_culinary(id: int, data: CulinaryUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    return CulinaryService(db).update(id, data)


@router.delete("/{id}", status_code=204, summary="Hapus kuliner (admin)")
def delete_culinary(id: int, db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    CulinaryService(db).delete(id)
