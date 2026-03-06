"""User management endpoints (admin only)."""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_admin
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.repositories.user_repository import UserRepository

router = APIRouter()


@router.get("/", response_model=List[UserResponse], summary="Daftar semua pengguna (admin)")
def list_users(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return UserRepository(db).get_active_users(skip, limit)


@router.get("/{user_id}", response_model=UserResponse, summary="Detail pengguna")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    repo = UserRepository(db)
    user = repo.get(user_id)
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Pengguna tidak ditemukan")
    return user


@router.put("/{user_id}", response_model=UserResponse, summary="Update pengguna (admin)")
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    repo = UserRepository(db)
    user = repo.get(user_id)
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Pengguna tidak ditemukan")
    if data.password:
        from app.core.security import hash_password
        user.hashed_password = hash_password(data.password)
    for field, value in data.model_dump(exclude_unset=True, exclude={"password"}).items():
        setattr(user, field, value)
    return repo.update(user)


@router.delete("/{user_id}", status_code=204, summary="Nonaktifkan pengguna (admin)")
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    repo = UserRepository(db)
    user = repo.get(user_id)
    if user:
        user.is_active = False
        repo.update(user)
