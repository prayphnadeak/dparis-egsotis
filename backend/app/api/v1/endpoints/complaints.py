"""Complaint (Pengaduan) endpoints."""
from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_admin, get_optional_user
from app.models.user import User
from app.schemas.complaint import ComplaintCreate, ComplaintUpdate, ComplaintResponse, ComplaintTrackRequest
from app.services.complaint_service import ComplaintService

router = APIRouter()


@router.post("/", response_model=ComplaintResponse, status_code=201, summary="Kirim pengaduan")
def submit_complaint(
    data: ComplaintCreate,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user),
):
    user_id = user.id if user else None
    return ComplaintService(db).submit(data, user_id)


@router.post("/track", response_model=ComplaintResponse, summary="Lacak pengaduan berdasarkan kode")
def track_complaint(req: ComplaintTrackRequest, db: Session = Depends(get_db)):
    return ComplaintService(db).track(req.tracking_code)


@router.get("/", response_model=List[ComplaintResponse], summary="Daftar pengaduan (admin)")
def list_complaints(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return ComplaintService(db).list_all(status, skip, limit)


@router.put("/{id}", response_model=ComplaintResponse, summary="Tanggapi pengaduan (admin)")
def respond_complaint(
    id: int,
    data: ComplaintUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return ComplaintService(db).respond(id, data)
