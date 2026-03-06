"""Authentication service – login and token refresh."""
from datetime import timedelta
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import verify_password, create_access_token, create_refresh_token, decode_token, hash_password
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.schemas.user import LoginRequest, TokenResponse, UserCreate
from app.core.config import settings
from jose import JWTError


class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def authenticate(self, username: str, password: str) -> User:
        user = self.repo.get_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username atau password salah",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Akun tidak aktif",
            )
        return user

    def login(self, req: LoginRequest) -> TokenResponse:
        user = self.authenticate(req.username, req.password)
        return TokenResponse(
            access_token=create_access_token(user.username),
            refresh_token=create_refresh_token(user.username),
        )

    def refresh(self, refresh_token: str) -> TokenResponse:
        try:
            payload = decode_token(refresh_token)
            if payload.get("type") != "refresh":
                raise ValueError("Bukan refresh token")
            username: str = payload["sub"]
        except (JWTError, KeyError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token tidak valid",
            )
        user = self.repo.get_by_username(username)
        if not user or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User tidak ditemukan")
        return TokenResponse(
            access_token=create_access_token(user.username),
            refresh_token=create_refresh_token(user.username),
        )

    def register(self, data: UserCreate) -> User:
        if self.repo.get_by_username(data.username):
            raise HTTPException(status_code=400, detail="Username sudah digunakan")
        if self.repo.get_by_email(data.email):
            raise HTTPException(status_code=400, detail="Email sudah digunakan")
        user = User(
            username=data.username,
            email=data.email,
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
        )
        return self.repo.create(user)
