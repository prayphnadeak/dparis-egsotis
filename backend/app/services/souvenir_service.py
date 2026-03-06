"""Souvenir (oleh-oleh) service."""
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.souvenir_repository import SouvenirRepository
from app.models.souvenir import SouvenirShop
from app.schemas.souvenir import SouvenirCreate, SouvenirUpdate


class SouvenirService:
    def __init__(self, db: Session):
        self.repo = SouvenirRepository(db)

    def list(self, query: str = "", skip: int = 0, limit: int = 100) -> List[SouvenirShop]:
        if query:
            return self.repo.search(query, skip, limit)
        return self.repo.get_active(skip, limit)

    def get_or_404(self, id: int) -> SouvenirShop:
        obj = self.repo.get(id)
        if not obj or not obj.is_active:
            raise HTTPException(status_code=404, detail="Toko oleh-oleh tidak ditemukan")
        return obj

    def create(self, data: SouvenirCreate) -> SouvenirShop:
        obj = SouvenirShop(**data.model_dump())
        return self.repo.create(obj)

    def update(self, id: int, data: SouvenirUpdate) -> SouvenirShop:
        obj = self.get_or_404(id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, field, value)
        return self.repo.update(obj)

    def delete(self, id: int) -> None:
        obj = self.get_or_404(id)
        obj.is_active = False
        self.repo.update(obj)
