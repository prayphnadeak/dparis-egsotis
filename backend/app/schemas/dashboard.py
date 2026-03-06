"""Pydantic schema for Dashboard summary."""
from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_accommodations: int
    total_tourism: int
    total_culinary: int
    total_infographics: int
    total_complaints: int
    pending_complaints: int
    resolved_complaints: int
    total_users: int
