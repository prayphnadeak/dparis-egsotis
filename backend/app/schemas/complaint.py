"""Pydantic schemas for Complaint."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class ComplaintBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    category: str
    message: str


class ComplaintCreate(ComplaintBase):
    pass


class ComplaintUpdate(BaseModel):
    status: Optional[str] = None
    response: Optional[str] = None


class ComplaintResponse(ComplaintBase):
    id: int
    status: str
    tracking_code: Optional[str] = None
    attachment_url: Optional[str] = None
    response: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ComplaintTrackRequest(BaseModel):
    tracking_code: str
