"""Authentication endpoints – login, refresh, register, me."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.schemas.user import LoginRequest, TokenResponse, UserCreate, UserResponse
from app.services.auth_service import AuthService
from app.models.user import User

router = APIRouter()


@router.post("/login", response_model=TokenResponse, summary="Login pengguna")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    return AuthService(db).login(req)


@router.post("/refresh", response_model=TokenResponse, summary="Refresh access token")
def refresh(body: dict, db: Session = Depends(get_db)):
    """Body: { "refresh_token": "..." }"""
    return AuthService(db).refresh(body.get("refresh_token", ""))


@router.post("/register", response_model=UserResponse, status_code=201, summary="Daftar pengguna baru")
def register(data: UserCreate, db: Session = Depends(get_db)):
    return AuthService(db).register(data)


@router.get("/me", response_model=UserResponse, summary="Info pengguna saat ini")
def me(current_user: User = Depends(get_current_user)):
    return current_user
