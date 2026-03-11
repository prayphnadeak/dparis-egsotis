"""Culinary repository."""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.culinary import CulinaryPlace
from app.repositories.base_repository import BaseRepository


class CulinaryRepository(BaseRepository[CulinaryPlace]):
    def __init__(self, db: Session):
        super().__init__(CulinaryPlace, db)

    def search(self, query: str, category: Optional[str] = None, skip: int = 0, limit: int = 200) -> List[CulinaryPlace]:
        q = self.db.query(CulinaryPlace).filter(CulinaryPlace.is_active == True)
        if query:
            q = q.filter(CulinaryPlace.name.ilike(f"%{query}%"))
        if category:
            q = q.filter(CulinaryPlace.category == category)
        return q.order_by(CulinaryPlace.name).offset(skip).limit(limit).all()

    def get_active(self, skip: int = 0, limit: int = 200) -> List[CulinaryPlace]:
        return (
            self.db.query(CulinaryPlace)
            .filter(CulinaryPlace.is_active == True)
            .order_by(CulinaryPlace.name)
            .offset(skip).limit(limit).all()
        )

    def count_active(self) -> int:
        return self.db.query(CulinaryPlace).filter(CulinaryPlace.is_active == True).count()
