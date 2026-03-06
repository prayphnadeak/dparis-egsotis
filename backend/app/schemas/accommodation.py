"""Pydantic schemas for Accommodation."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class FacilityMixin(BaseModel):
    hot_water: bool = False
    tv_cable: bool = False
    bed: bool = True
    free_wifi: bool = False
    restaurant: bool = False
    swimming_pool: bool = False
    gym: bool = False
    meeting_room: bool = False


class AccommodationBase(FacilityMixin):
    name: str
    category: str
    total_rooms: int = 0
    total_beds: int = 0
    phone: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    maps_link: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class AccommodationCreate(AccommodationBase):
    pass


class AccommodationUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    total_rooms: Optional[int] = None
    total_beds: Optional[int] = None
    phone: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    maps_link: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    hot_water: Optional[bool] = None
    tv_cable: Optional[bool] = None
    bed: Optional[bool] = None
    free_wifi: Optional[bool] = None
    restaurant: Optional[bool] = None
    swimming_pool: Optional[bool] = None
    gym: Optional[bool] = None
    meeting_room: Optional[bool] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class AccommodationResponse(AccommodationBase):
    id: int
    image_url: Optional[str] = None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
