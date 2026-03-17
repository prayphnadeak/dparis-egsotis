"""Souvenir shop (Toko Oleh-Oleh) model."""
from sqlalchemy import Boolean, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class SouvenirShop(Base, TimestampMixin):
    __tablename__ = "souvenir_shops"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)

    # Location link (Google Maps)
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

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self) -> str:
        return f"<SouvenirShop {self.name!r}>"
