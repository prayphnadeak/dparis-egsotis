"""Accommodation repository."""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.accommodation import Accommodation
from app.repositories.base_repository import BaseRepository


class AccommodationRepository(BaseRepository[Accommodation]):
    def __init__(self, db: Session):
        super().__init__(Accommodation, db)

    def search(self, query: str, category: Optional[str] = None, skip: int = 0, limit: int = 20) -> List[Accommodation]:
        q = self.db.query(Accommodation).filter(Accommodation.is_active == True)
        if query:
            q = q.filter(Accommodation.name.ilike(f"%{query}%"))
        if category:
            q = q.filter(Accommodation.category == category)
        return q.order_by(Accommodation.name).offset(skip).limit(limit).all()

    def get_active(self, skip: int = 0, limit: int = 20) -> List[Accommodation]:
        return (
            self.db.query(Accommodation)
            .filter(Accommodation.is_active == True)
            .order_by(Accommodation.name)
            .offset(skip).limit(limit).all()
        )

    def count_active(self) -> int:
        return self.db.query(Accommodation).filter(Accommodation.is_active == True).count()
