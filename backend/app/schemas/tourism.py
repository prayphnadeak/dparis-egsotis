"""Pydantic schemas for Tourism."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TourismBase(BaseModel):
    name: str
    category: str
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


class TourismResponse(TourismBase):
    id: int
    maps_link: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
