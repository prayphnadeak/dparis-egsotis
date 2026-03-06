"""Accommodation CRUD endpoints."""
from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_admin
from app.models.user import User
from app.schemas.accommodation import AccommodationCreate, AccommodationUpdate, AccommodationResponse
from app.services.accommodation_service import AccommodationService

router = APIRouter()


@router.get("/", response_model=List[AccommodationResponse], summary="Daftar akomodasi")
def list_accommodations(
    q: str = "",
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    return AccommodationService(db).list(q, category, skip, limit)


@router.get("/{id}", response_model=AccommodationResponse, summary="Detail akomodasi")
def get_accommodation(id: int, db: Session = Depends(get_db)):
    return AccommodationService(db).get_or_404(id)


@router.post("/", response_model=AccommodationResponse, status_code=201, summary="Tambah akomodasi (admin)")
def create_accommodation(
    data: AccommodationCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return AccommodationService(db).create(data)


@router.put("/{id}", response_model=AccommodationResponse, summary="Update akomodasi (admin)")
def update_accommodation(
    id: int,
    data: AccommodationUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return AccommodationService(db).update(id, data)


@router.delete("/{id}", status_code=204, summary="Hapus akomodasi (admin)")
def delete_accommodation(
    id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    AccommodationService(db).delete(id)
