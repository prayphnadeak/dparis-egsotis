"""Transportation model."""
from sqlalchemy import Boolean, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

class Transportation(Base, TimestampMixin):
    __tablename__ = "transportations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # Moda Transportasi
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    
    # Routes (Rute)
    route_palembang: Mapped[bool] = mapped_column(Boolean, default=False)
    route_bengkulu: Mapped[bool] = mapped_column(Boolean, default=False)
    route_lampung: Mapped[bool] = mapped_column(Boolean, default=False)
    route_jabodetabek: Mapped[bool] = mapped_column(Boolean, default=False)
    route_jawa: Mapped[bool] = mapped_column(Boolean, default=False)
    
    phone: Mapped[str] = mapped_column(String(50), nullable=True)
    maps_link: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # GPS (if applicable)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)

    # Distance to landmarks (in km)
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
        return f"<Transportation {self.name!r}>"
