"""Pydantic schemas for Culinary."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CulinaryBase(BaseModel):
    name: str
    category: str
    description: Optional[str] = None
    phone: Optional[str] = None
    opening_hours: Optional[str] = None
    address: Optional[str] = None
    menu_highlights: Optional[str] = None
    maps_link: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class CulinaryCreate(CulinaryBase):
    pass


class CulinaryUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    phone: Optional[str] = None
    opening_hours: Optional[str] = None
    address: Optional[str] = None
    menu_highlights: Optional[str] = None
    maps_link: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class CulinaryResponse(CulinaryBase):
    id: int
    maps_link: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
