"""Complaint repository."""
import secrets
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.complaint import Complaint, ComplaintStatus
from app.repositories.base_repository import BaseRepository


class ComplaintRepository(BaseRepository[Complaint]):
    def __init__(self, db: Session):
        super().__init__(Complaint, db)

    def get_by_tracking_code(self, code: str) -> Optional[Complaint]:
        return self.db.query(Complaint).filter(Complaint.tracking_code == code).first()

    def get_by_status(self, status: ComplaintStatus, skip: int = 0, limit: int = 20) -> List[Complaint]:
        return (
            self.db.query(Complaint)
            .filter(Complaint.status == status)
            .order_by(Complaint.created_at.desc())
            .offset(skip).limit(limit).all()
        )

    def get_all_ordered(self, skip: int = 0, limit: int = 20) -> List[Complaint]:
        return (
            self.db.query(Complaint)
            .order_by(Complaint.created_at.desc())
            .offset(skip).limit(limit).all()
        )

    def count_by_status(self, status: ComplaintStatus) -> int:
        return self.db.query(Complaint).filter(Complaint.status == status).count()

    @staticmethod
    def generate_tracking_code() -> str:
        return "TRK-" + secrets.token_hex(4).upper()
