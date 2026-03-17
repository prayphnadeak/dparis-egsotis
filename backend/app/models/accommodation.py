"""Accommodation model."""
from sqlalchemy import Boolean, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Accommodation(Base, TimestampMixin):
    __tablename__ = "accommodations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    total_rooms: Mapped[int] = mapped_column(Integer, default=0)
    total_beds: Mapped[int] = mapped_column(Integer, default=0)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    address: Mapped[str] = mapped_column(String(300), nullable=True)

    # Facilities
    hot_water: Mapped[bool] = mapped_column(Boolean, default=False)
    tv_cable: Mapped[bool] = mapped_column(Boolean, default=False)
    bed: Mapped[bool] = mapped_column(Boolean, default=True)
    free_wifi: Mapped[bool] = mapped_column(Boolean, default=False)
    restaurant: Mapped[bool] = mapped_column(Boolean, default=False)
    swimming_pool: Mapped[bool] = mapped_column(Boolean, default=False)
    gym: Mapped[bool] = mapped_column(Boolean, default=False)
    meeting_room: Mapped[bool] = mapped_column(Boolean, default=False)

    # Location link
    maps_link: Mapped[str] = mapped_column(String(500), nullable=True)

    # GPS
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)

    # Rating
    rating: Mapped[float] = mapped_column(Float, nullable=True)

    # Distance to landmarks (in km)
    dist_gunung_dempo: Mapped[float] = mapped_column(Float, nullable=True)
    dist_pasar_dempo_permai: Mapped[float] = mapped_column(Float, nullable=True)
    dist_bandara_atung_bungsu: Mapped[float] = mapped_column(Float, nullable=True)
    dist_rsud_besemah: Mapped[float] = mapped_column(Float, nullable=True)
    dist_spbu_air_perikan: Mapped[float] = mapped_column(Float, nullable=True)
    dist_spbu_simpang_manna: Mapped[float] = mapped_column(Float, nullable=True)
    dist_spbu_pengandonan: Mapped[float] = mapped_column(Float, nullable=True)
    dist_spbu_karang_dalo: Mapped[float] = mapped_column(Float, nullable=True)

    # Media
    image_url: Mapped[str] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self) -> str:
        return f"<Accommodation {self.name!r}>"
