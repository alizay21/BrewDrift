from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    visited_place_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("visited_places.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    personal_rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    experience_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    personal_tags: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, onupdate=_now, nullable=False
    )

    visit: Mapped["Visit"] = relationship("Visit", back_populates="review")
    photos: Mapped[list["Photo"]] = relationship(
        "Photo", back_populates="review", cascade="all, delete-orphan"
    )
