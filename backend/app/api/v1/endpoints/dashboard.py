"""Dashboard statistics endpoint (admin)."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_admin
from app.models.user import User
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import DashboardService

router = APIRouter()


@router.get("/", response_model=DashboardResponse, summary="Ringkasan statistik dashboard (admin)")
def get_dashboard(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return DashboardService(db).get_summary()
