"""Tourism service."""
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.tourism_repository import TourismRepository
from app.models.tourism import TourismObject
from app.schemas.tourism import TourismCreate, TourismUpdate


class TourismService:
    def __init__(self, db: Session):
        self.repo = TourismRepository(db)

    def list(self, query: str = "", category: Optional[str] = None, skip: int = 0, limit: int = 200) -> List[TourismObject]:
        if query or category:
            return self.repo.search(query, category, skip, limit)
        return self.repo.get_active(skip, limit)

    def get_or_404(self, id: int) -> TourismObject:
        obj = self.repo.get(id)
        if not obj or not obj.is_active:
            raise HTTPException(status_code=404, detail="Objek wisata tidak ditemukan")
        return obj

    def create(self, data: TourismCreate) -> TourismObject:
        obj = TourismObject(**data.model_dump())
        return self.repo.create(obj)

    def update(self, id: int, data: TourismUpdate) -> TourismObject:
        obj = self.get_or_404(id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, field, value)
        return self.repo.update(obj)

    def delete(self, id: int) -> None:
        obj = self.get_or_404(id)
        obj.is_active = False
        self.repo.update(obj)
