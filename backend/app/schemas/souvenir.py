"""Pydantic schemas for Souvenir (Oleh-Oleh)."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SouvenirBase(BaseModel):
    name: str
    rating: Optional[float] = None
    maps_link: Optional[str] = None


class SouvenirCreate(SouvenirBase):
    pass


class SouvenirUpdate(BaseModel):
    name: Optional[str] = None
    rating: Optional[float] = None
    maps_link: Optional[str] = None
    is_active: Optional[bool] = None


class SouvenirResponse(SouvenirBase):
    id: int
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

    # Hit view count
    view_count: int = 1

    model_config = {"from_attributes": True}
