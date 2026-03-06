"""Infographic endpoints."""
from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_admin
from app.models.user import User
from app.schemas.infographic import InfographicCreate, InfographicUpdate, InfographicResponse
from app.services.infographic_service import InfographicService

router = APIRouter()


@router.get("/", response_model=List[InfographicResponse], summary="Daftar infografis")
def list_infographics(year: Optional[int] = None, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return InfographicService(db).list(year, skip, limit)


@router.get("/{id}", response_model=InfographicResponse, summary="Detail infografis")
def get_infographic(id: int, db: Session = Depends(get_db)):
    return InfographicService(db).get_or_404(id)


@router.post("/{id}/download", response_model=InfographicResponse, summary="Hitung unduhan infografis")
def track_download(id: int, db: Session = Depends(get_db)):
    return InfographicService(db).track_download(id)


@router.post("/", response_model=InfographicResponse, status_code=201, summary="Tambah infografis (admin)")
def create_infographic(data: InfographicCreate, db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    return InfographicService(db).create(data)


@router.put("/{id}", response_model=InfographicResponse, summary="Update infografis (admin)")
def update_infographic(id: int, data: InfographicUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    return InfographicService(db).update(id, data)


@router.delete("/{id}", status_code=204, summary="Hapus infografis (admin)")
def delete_infographic(id: int, db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    InfographicService(db).delete(id)
