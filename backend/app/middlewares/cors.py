"""CORS configuration helper (used in main.py via CORSMiddleware)."""
from app.core.config import settings

CORS_CONFIG = {
    "allow_origins": settings.CORS_ORIGINS,
    "allow_credentials": True,
    "allow_methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    "allow_headers": ["Authorization", "Content-Type", "Accept", "X-Requested-With"],
    "expose_headers": ["X-Total-Count", "X-Page", "X-Page-Size"],
    "max_age": 86400,
}
