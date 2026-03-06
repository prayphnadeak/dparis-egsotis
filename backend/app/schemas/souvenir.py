"""Pydantic schemas for Souvenir (Oleh-Oleh)."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SouvenirBase(BaseModel):
    name: str
    maps_link: Optional[str] = None


class SouvenirCreate(SouvenirBase):
    pass


class SouvenirUpdate(BaseModel):
    name: Optional[str] = None
    maps_link: Optional[str] = None
    is_active: Optional[bool] = None


class SouvenirResponse(SouvenirBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
