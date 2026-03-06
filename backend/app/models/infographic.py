"""Infographic model."""
from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Infographic(Base, TimestampMixin):
    __tablename__ = "infographics"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    year: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    image_url: Mapped[str] = mapped_column(String(500), nullable=True)
    pdf_url: Mapped[str] = mapped_column(String(500), nullable=True)
    tags: Mapped[str] = mapped_column(String(500), nullable=True)  # comma-separated
    download_count: Mapped[int] = mapped_column(Integer, default=0)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self) -> str:
        return f"<Infographic {self.title!r} [{self.year}]>"
