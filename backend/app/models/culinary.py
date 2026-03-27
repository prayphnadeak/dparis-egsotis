"""Culinary place model."""
from sqlalchemy import Boolean, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class CulinaryPlace(Base, TimestampMixin):
    __tablename__ = "culinary_places"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    opening_hours: Mapped[str] = mapped_column(String(100), nullable=True)
    address: Mapped[str] = mapped_column(String(300), nullable=True)
    menu_highlights: Mapped[str] = mapped_column(Text, nullable=True)

    # GPS
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)

    # Location link
    maps_link: Mapped[str] = mapped_column(String(1000), nullable=True)

    # Rating
    rating: Mapped[float] = mapped_column(Float, nullable=True)

    # Distance to landmarks (km)
    dist_gunung_dempo: Mapped[float] = mapped_column(Float, nullable=True)
    dist_pasar_dempo_permai: Mapped[float] = mapped_column(Float, nullable=True)
    dist_bandara_atung_bungsu: Mapped[float] = mapped_column(Float, nullable=True)
    dist_rsud_besemah: Mapped[float] = mapped_column(Float, nullable=True)
    dist_spbu_air_perikan: Mapped[float] = mapped_column(Float, nullable=True)
    dist_spbu_simpang_manna: Mapped[float] = mapped_column(Float, nullable=True)
    dist_spbu_pengandonan: Mapped[float] = mapped_column(Float, nullable=True)
    dist_spbu_karang_dalo: Mapped[float] = mapped_column(Float, nullable=True)

    # Hit view count
    view_count: Mapped[int] = mapped_column(default=1, nullable=False)

    # Media
    image_url: Mapped[str] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self) -> str:
        return f"<CulinaryPlace {self.name!r}>"
