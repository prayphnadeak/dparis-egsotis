"""Tourism repository."""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.tourism import TourismObject
from app.repositories.base_repository import BaseRepository


class TourismRepository(BaseRepository[TourismObject]):
    def __init__(self, db: Session):
        super().__init__(TourismObject, db)

    def search(self, query: str, category: Optional[str] = None, skip: int = 0, limit: int = 20) -> List[TourismObject]:
        q = self.db.query(TourismObject).filter(TourismObject.is_active == True)
        if query:
            q = q.filter(TourismObject.name.ilike(f"%{query}%"))
        if category:
            q = q.filter(TourismObject.category == category)
        return q.order_by(TourismObject.name).offset(skip).limit(limit).all()

    def get_active(self, skip: int = 0, limit: int = 20) -> List[TourismObject]:
        return (
            self.db.query(TourismObject)
            .filter(TourismObject.is_active == True)
            .order_by(TourismObject.name)
            .offset(skip).limit(limit).all()
        )

    def count_active(self) -> int:
        return self.db.query(TourismObject).filter(TourismObject.is_active == True).count()
