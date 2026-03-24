"""User Log model for tracking daily visitors and downloaders."""
from sqlalchemy import Date, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class UserLog(Base):
    __tablename__ = "user_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    date: Mapped[str] = mapped_column(Date, unique=True, index=True, nullable=False)
    visitor_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    downloader_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    def __repr__(self) -> str:
        return f"<UserLog date={self.date} visitors={self.visitor_count} downloaders={self.downloader_count}>"
