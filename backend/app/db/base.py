"""Import all models so Alembic can detect them."""
from app.models.base import Base  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.accommodation import Accommodation  # noqa: F401
from app.models.tourism import TourismObject  # noqa: F401
from app.models.culinary import CulinaryPlace  # noqa: F401
from app.models.infographic import Infographic  # noqa: F401
from app.models.complaint import Complaint  # noqa: F401
from app.models.audit_log import AuditLog  # noqa: F401
from app.models.souvenir import SouvenirShop  # noqa: F401
from app.models.user_log import UserLog  # noqa: F401
