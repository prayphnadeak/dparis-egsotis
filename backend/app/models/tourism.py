"""Tourism object model."""
from sqlalchemy import Boolean, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class TourismObject(Base, TimestampMixin):
    __tablename__ = "tourism_objects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    address: Mapped[str] = mapped_column(String(300), nullable=True)
    opening_hours: Mapped[str] = mapped_column(String(100), nullable=True)
    ticket_price: Mapped[float] = mapped_column(Float, default=0.0, nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)

    # GPS
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)

    # Location link
    maps_link: Mapped[str] = mapped_column(String(1000), nullable=True)

    # Media
    image_url: Mapped[str] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def __repr__(self) -> str:
        return f"<TourismObject {self.name!r}>"
