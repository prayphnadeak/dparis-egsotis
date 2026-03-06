"""Souvenir shop repository."""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.souvenir import SouvenirShop
from app.repositories.base_repository import BaseRepository


class SouvenirRepository(BaseRepository[SouvenirShop]):
    def __init__(self, db: Session):
        super().__init__(SouvenirShop, db)

    def search(self, query: str, skip: int = 0, limit: int = 100) -> List[SouvenirShop]:
        q = self.db.query(SouvenirShop).filter(SouvenirShop.is_active == True)
        if query:
            q = q.filter(SouvenirShop.name.ilike(f"%{query}%"))
        return q.order_by(SouvenirShop.name).offset(skip).limit(limit).all()

    def get_active(self, skip: int = 0, limit: int = 100) -> List[SouvenirShop]:
        return (
            self.db.query(SouvenirShop)
            .filter(SouvenirShop.is_active == True)
            .order_by(SouvenirShop.name)
            .offset(skip).limit(limit).all()
        )

    def count_active(self) -> int:
        return self.db.query(SouvenirShop).filter(SouvenirShop.is_active == True).count()
