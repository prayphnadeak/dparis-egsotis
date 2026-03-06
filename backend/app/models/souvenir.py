"""Souvenir shop (Toko Oleh-Oleh) model."""
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class SouvenirShop(Base, TimestampMixin):
    __tablename__ = "souvenir_shops"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)

    # Location link (Google Maps)
    maps_link: Mapped[str] = mapped_column(String(1000), nullable=True)

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self) -> str:
        return f"<SouvenirShop {self.name!r}>"
