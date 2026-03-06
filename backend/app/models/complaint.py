"""Complaint model."""
import enum

from sqlalchemy import Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class ComplaintStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROCESS = "in_process"
    RESOLVED = "resolved"
    REJECTED = "rejected"


class Complaint(Base, TimestampMixin):
    __tablename__ = "complaints"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    address: Mapped[str] = mapped_column(String(300), nullable=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    attachment_url: Mapped[str] = mapped_column(String(500), nullable=True)
    status: Mapped[ComplaintStatus] = mapped_column(
        Enum(ComplaintStatus), default=ComplaintStatus.PENDING, nullable=False, index=True
    )
    response: Mapped[str] = mapped_column(Text, nullable=True)
    tracking_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=True, index=True)

    # Optional FK to registered user
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    user = relationship("User", back_populates="complaints")

    def __repr__(self) -> str:
        return f"<Complaint #{self.id} [{self.status}]>"
