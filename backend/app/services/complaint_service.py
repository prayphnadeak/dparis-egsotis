"""Complaint service."""
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.complaint_repository import ComplaintRepository
from app.models.complaint import Complaint, ComplaintStatus
from app.schemas.complaint import ComplaintCreate, ComplaintUpdate


class ComplaintService:
    def __init__(self, db: Session):
        self.repo = ComplaintRepository(db)

    def submit(self, data: ComplaintCreate, user_id: Optional[int] = None) -> Complaint:
        tracking_code = ComplaintRepository.generate_tracking_code()
        obj = Complaint(
            **data.model_dump(),
            tracking_code=tracking_code,
            user_id=user_id,
        )
        return self.repo.create(obj)

    def track(self, tracking_code: str) -> Complaint:
        obj = self.repo.get_by_tracking_code(tracking_code)
        if not obj:
            raise HTTPException(status_code=404, detail="Kode pengaduan tidak ditemukan")
        return obj

    def list_all(self, status: Optional[str] = None, skip: int = 0, limit: int = 20) -> List[Complaint]:
        if status:
            try:
                s = ComplaintStatus(status)
                return self.repo.get_by_status(s, skip, limit)
            except ValueError:
                raise HTTPException(status_code=400, detail="Status tidak valid")
        return self.repo.get_all_ordered(skip, limit)

    def respond(self, id: int, data: ComplaintUpdate) -> Complaint:
        obj = self.repo.get(id)
        if not obj:
            raise HTTPException(status_code=404, detail="Pengaduan tidak ditemukan")
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, field, value)
        return self.repo.update(obj)
