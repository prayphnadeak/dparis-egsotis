"""Pydantic schemas for Tourism."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TourismBase(BaseModel):
    name: str
    category: str
    daya_tarik: Optional[str] = None
    rating: Optional[float] = None
    description: Optional[str] = None
    address: Optional[str] = None
    opening_hours: Optional[str] = None
    ticket_price: Optional[float] = 0.0
    phone: Optional[str] = None
    maps_link: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class TourismCreate(TourismBase):
    pass


class TourismUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    daya_tarik: Optional[str] = None
    rating: Optional[float] = None
    description: Optional[str] = None
    address: Optional[str] = None
    opening_hours: Optional[str] = None
    ticket_price: Optional[float] = None
    phone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    maps_link: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None

    # Wisata types
    wisata_alam: Optional[bool] = None
    wisata_budaya: Optional[bool] = None
    wisata_buatan: Optional[bool] = None


class TourismResponse(TourismBase):
    id: int
    maps_link: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool
    created_at: datetime

    # Distance to landmarks (km)
    dist_gunung_dempo: Optional[float] = None
    dist_pasar_dempo_permai: Optional[float] = None
    dist_bandara_atung_bungsu: Optional[float] = None
    dist_rsud_besemah: Optional[float] = None
    dist_spbu_air_perikan: Optional[float] = None
    dist_spbu_simpang_manna: Optional[float] = None
    dist_spbu_pengandonan: Optional[float] = None
    dist_spbu_karang_dalo: Optional[float] = None

    # Wisata types
    wisata_alam: Optional[bool] = False
    wisata_budaya: Optional[bool] = False
    wisata_buatan: Optional[bool] = False

    model_config = {"from_attributes": True}
