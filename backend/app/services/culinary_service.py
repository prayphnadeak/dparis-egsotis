"""Culinary service."""
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.culinary_repository import CulinaryRepository
from app.models.culinary import CulinaryPlace
from app.schemas.culinary import CulinaryCreate, CulinaryUpdate


class CulinaryService:
    def __init__(self, db: Session):
        self.repo = CulinaryRepository(db)

    def list(self, query: str = "", category: Optional[str] = None, skip: int = 0, limit: int = 200) -> List[CulinaryPlace]:
        if query or category:
            return self.repo.search(query, category, skip, limit)
        return self.repo.get_active(skip, limit)

    def get_or_404(self, id: int) -> CulinaryPlace:
        obj = self.repo.get(id)
        if not obj or not obj.is_active:
            raise HTTPException(status_code=404, detail="Tempat kuliner tidak ditemukan")
        return obj

    def create(self, data: CulinaryCreate) -> CulinaryPlace:
        obj = CulinaryPlace(**data.model_dump())
        return self.repo.create(obj)

    def update(self, id: int, data: CulinaryUpdate) -> CulinaryPlace:
        obj = self.get_or_404(id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, field, value)
        return self.repo.update(obj)

    def delete(self, id: int) -> None:
        obj = self.get_or_404(id)
        obj.is_active = False
        self.repo.update(obj)
