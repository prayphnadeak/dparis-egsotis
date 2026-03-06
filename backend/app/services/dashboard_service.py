"""Dashboard statistics service."""
from sqlalchemy.orm import Session

from app.models.accommodation import Accommodation
from app.models.tourism import TourismObject
from app.models.culinary import CulinaryPlace
from app.models.infographic import Infographic
from app.models.complaint import Complaint, ComplaintStatus
from app.models.user import User
from app.schemas.dashboard import DashboardResponse


class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def get_summary(self) -> DashboardResponse:
        return DashboardResponse(
            total_accommodations=self.db.query(Accommodation).filter(Accommodation.is_active == True).count(),
            total_tourism=self.db.query(TourismObject).filter(TourismObject.is_active == True).count(),
            total_culinary=self.db.query(CulinaryPlace).filter(CulinaryPlace.is_active == True).count(),
            total_infographics=self.db.query(Infographic).filter(Infographic.is_published == True).count(),
            total_complaints=self.db.query(Complaint).count(),
            pending_complaints=self.db.query(Complaint).filter(Complaint.status == ComplaintStatus.PENDING).count(),
            resolved_complaints=self.db.query(Complaint).filter(Complaint.status == ComplaintStatus.RESOLVED).count(),
            total_users=self.db.query(User).filter(User.is_active == True).count(),
        )
