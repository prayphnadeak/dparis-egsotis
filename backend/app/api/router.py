"""API router – aggregates all v1 routes."""
from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    accommodations,
    tourism,
    culinary,
    infographics,
    complaints,
    dashboard,
    souvenirs,
    media,
    statistics,
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/v1/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/v1/users", tags=["Users"])
api_router.include_router(accommodations.router, prefix="/v1/accommodations", tags=["Akomodasi"])
api_router.include_router(tourism.router, prefix="/v1/tourism", tags=["Wisata"])
api_router.include_router(culinary.router, prefix="/v1/culinary", tags=["Kuliner"])
api_router.include_router(infographics.router, prefix="/v1/infographics", tags=["Infografis"])
api_router.include_router(complaints.router, prefix="/v1/complaints", tags=["Pengaduan"])
api_router.include_router(dashboard.router, prefix="/v1/dashboard", tags=["Dashboard"])
api_router.include_router(souvenirs.router, prefix="/v1/souvenirs", tags=["Oleh-Oleh"])
api_router.include_router(media.router, prefix="/v1/media", tags=["Media"])
api_router.include_router(statistics.router, prefix="/v1/statistics", tags=["Statistik"])
