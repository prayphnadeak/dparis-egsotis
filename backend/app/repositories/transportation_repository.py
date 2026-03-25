"""Transportation repository."""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.transportation import Transportation
from app.repositories.base_repository import BaseRepository


class TransportationRepository(BaseRepository[Transportation]):
    def __init__(self, db: Session):
        super().__init__(Transportation, db)

    def search(self, query: str, category: Optional[str] = None, skip: int = 0, limit: int = 200) -> List[Transportation]:
        q = self.db.query(Transportation).filter(Transportation.is_active == True)
        if query:
            q = q.filter(Transportation.name.ilike(f"%{query}%"))
        if category:
            q = q.filter(Transportation.category == category)
        return q.order_by(Transportation.name).offset(skip).limit(limit).all()

    def get_active(self, skip: int = 0, limit: int = 200) -> List[Transportation]:
        return (
            self.db.query(Transportation)
            .filter(Transportation.is_active == True)
            .order_by(Transportation.name)
            .offset(skip).limit(limit).all()
        )

    def count_active(self) -> int:
        return self.db.query(Transportation).filter(Transportation.is_active == True).count()
