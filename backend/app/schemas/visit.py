from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class CreateVisitRequest(BaseModel):
    provider: str = Field(default="google", max_length=50)
    provider_place_id: str = Field(min_length=1, max_length=255)
    place_name_snapshot: str = Field(min_length=1, max_length=255)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    visited_at: datetime


class UpdateVisitRequest(BaseModel):
    visited_at: datetime | None = None


class VisitResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    provider: str
    provider_place_id: str
    place_name_snapshot: str
    latitude: float
    longitude: float
    visited_at: datetime
    created_at: datetime
