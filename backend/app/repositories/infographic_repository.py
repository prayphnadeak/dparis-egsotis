"""Infographic repository."""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.infographic import Infographic
from app.repositories.base_repository import BaseRepository


class InfographicRepository(BaseRepository[Infographic]):
    def __init__(self, db: Session):
        super().__init__(Infographic, db)

    def get_published(self, year: Optional[int] = None, skip: int = 0, limit: int = 20) -> List[Infographic]:
        q = self.db.query(Infographic).filter(Infographic.is_published == True)
        if year:
            q = q.filter(Infographic.year == year)
        return q.order_by(Infographic.year.desc(), Infographic.title).offset(skip).limit(limit).all()

    def increment_download(self, infographic: Infographic) -> Infographic:
        infographic.download_count += 1
        self.db.commit()
        self.db.refresh(infographic)
        return infographic

    def count_published(self) -> int:
        return self.db.query(Infographic).filter(Infographic.is_published == True).count()
