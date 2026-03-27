"""Souvenir (Oleh-Oleh) endpoints."""
from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_admin
from app.models.user import User
from app.schemas.souvenir import SouvenirCreate, SouvenirUpdate, SouvenirResponse
from app.services.souvenir_service import SouvenirService

router = APIRouter()


@router.get("/", response_model=List[SouvenirResponse], summary="Daftar toko oleh-oleh")
def list_souvenirs(q: str = "", skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    return SouvenirService(db).list(q, skip, limit)


@router.get("/{id}", response_model=SouvenirResponse, summary="Detail toko oleh-oleh")
def get_souvenir(id: int, db: Session = Depends(get_db)):
    return SouvenirService(db).get_or_404(id)


@router.post("/{id}/hit", summary="Tambah hit view oleh-oleh")
def hit_souvenir(id: int, db: Session = Depends(get_db)):
    from app.models.souvenir import SouvenirShop
    obj = db.get(SouvenirShop, id)
    if obj is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Not found")
    obj.view_count = (obj.view_count or 1) + 1
    db.commit()
    db.refresh(obj)
    return {"view_count": obj.view_count}


@router.post("/", response_model=SouvenirResponse, status_code=201, summary="Tambah toko oleh-oleh (admin)")
def create_souvenir(data: SouvenirCreate, db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    return SouvenirService(db).create(data)


@router.put("/{id}", response_model=SouvenirResponse, summary="Update toko oleh-oleh (admin)")
def update_souvenir(id: int, data: SouvenirUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    return SouvenirService(db).update(id, data)


@router.delete("/{id}", status_code=204, summary="Hapus toko oleh-oleh (admin)")
def delete_souvenir(id: int, db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    SouvenirService(db).delete(id)
