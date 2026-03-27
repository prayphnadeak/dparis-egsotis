"""Transportation CRUD endpoints."""
from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_admin
from app.models.user import User
from app.schemas.transportation import TransportationCreate, TransportationUpdate, TransportationResponse
from app.services.transportation_service import TransportationService

router = APIRouter()

@router.get("/", response_model=List[TransportationResponse], summary="Daftar transportasi")
def list_transportations(
    q: str = "",
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 200,
    db: Session = Depends(get_db),
):
    return TransportationService(db).list(q, category, skip, limit)

@router.get("/{id}", response_model=TransportationResponse, summary="Detail transportasi")
def get_transportation(id: int, db: Session = Depends(get_db)):
    return TransportationService(db).get_or_404(id)

@router.post("/{id}/hit", summary="Tambah hit view transportasi")
def hit_transportation(id: int, db: Session = Depends(get_db)):
    from app.models.transportation import Transportation
    obj = db.get(Transportation, id)
    if obj is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Not found")
    obj.view_count = (obj.view_count or 1) + 1
    db.commit()
    db.refresh(obj)
    return {"view_count": obj.view_count}

@router.post("/", response_model=TransportationResponse, status_code=201, summary="Tambah transportasi (admin)")
def create_transportation(
    data: TransportationCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return TransportationService(db).create(data)

@router.put("/{id}", response_model=TransportationResponse, summary="Update transportasi (admin)")
def update_transportation(
    id: int,
    data: TransportationUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return TransportationService(db).update(id, data)

@router.delete("/{id}", status_code=204, summary="Hapus transportasi (admin)")
def delete_transportation(
    id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    TransportationService(db).delete(id)
