"""Pydantic schemas for Infographic."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class InfographicBase(BaseModel):
    title: str
    description: Optional[str] = None
    year: Optional[int] = None
    tags: Optional[str] = None


class InfographicCreate(InfographicBase):
    pass


class InfographicUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    year: Optional[int] = None
    tags: Optional[str] = None
    image_url: Optional[str] = None
    pdf_url: Optional[str] = None
    is_published: Optional[bool] = None


class InfographicResponse(InfographicBase):
    id: int
    image_url: Optional[str] = None
    pdf_url: Optional[str] = None
    download_count: int
    is_published: bool
    created_at: datetime

    model_config = {"from_attributes": True}
