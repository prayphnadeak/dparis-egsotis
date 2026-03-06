"""Infographic service."""
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.infographic_repository import InfographicRepository
from app.models.infographic import Infographic
from app.schemas.infographic import InfographicCreate, InfographicUpdate


class InfographicService:
    def __init__(self, db: Session):
        self.repo = InfographicRepository(db)

    def list(self, year: Optional[int] = None, skip: int = 0, limit: int = 20) -> List[Infographic]:
        return self.repo.get_published(year, skip, limit)

    def get_or_404(self, id: int) -> Infographic:
        obj = self.repo.get(id)
        if not obj:
            raise HTTPException(status_code=404, detail="Infografis tidak ditemukan")
        return obj

    def create(self, data: InfographicCreate) -> Infographic:
        obj = Infographic(**data.model_dump())
        return self.repo.create(obj)

    def update(self, id: int, data: InfographicUpdate) -> Infographic:
        obj = self.get_or_404(id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, field, value)
        return self.repo.update(obj)

    def delete(self, id: int) -> None:
        obj = self.get_or_404(id)
        self.repo.delete(obj)

    def track_download(self, id: int) -> Infographic:
        obj = self.get_or_404(id)
        return self.repo.increment_download(obj)
