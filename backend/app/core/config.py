"""Application configuration using pydantic-settings."""
from typing import List, Union
import json
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # App
    APP_NAME: str = "D'PARIS EGSOTIS API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    DATABASE_URL: str = "sqlite:///./dparis.db"

    # JWT
    SECRET_KEY: str = "dparis-egsotis-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Admin
    ADMIN_USERNAME: str = "admin"
    ADMIN_EMAIL: str = "admin@dparis.id"
    ADMIN_PASSWORD: str = "Admin@12345"

    # WhatsApp
    WHATSAPP_NUMBER: str = "6282XXXXXXXXX"

    # Google Maps
    GOOGLE_MAPS_API_KEY: str = ""

    # Supabase (Storage & Auth)
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_BUCKET: str = "dparis"

    # File upload
    UPLOAD_DIR: str = "static/uploads"
    MAX_UPLOAD_SIZE_MB: int = 5
    ALLOWED_IMAGE_TYPES: str = "image/jpeg,image/png,image/webp"

    # CORS
    CORS_ORIGINS: List[str] = ["*"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, str) and v.startswith("["):
            return json.loads(v)
        return v

    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    @property
    def allowed_image_types_list(self) -> List[str]:
        return [t.strip() for t in self.ALLOWED_IMAGE_TYPES.split(",")]

    @property
    def max_upload_bytes(self) -> int:
        return self.MAX_UPLOAD_SIZE_MB * 1024 * 1024


settings = Settings()
