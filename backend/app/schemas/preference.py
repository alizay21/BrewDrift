from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class PreferenceResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    user_id: str
    preferred_vibes: list[str]
    preferred_max_distance_km: int
    preferred_min_rating: float
    onboarding_completed: bool
    location_permission_asked: bool
    created_at: datetime
    updated_at: datetime


class UpdatePreferenceRequest(BaseModel):
    preferred_vibes: list[str] | None = None
    preferred_max_distance_km: int | None = Field(default=None, ge=1, le=100)
    preferred_min_rating: float | None = Field(default=None, ge=0.0, le=5.0)
    onboarding_completed: bool | None = None
    location_permission_asked: bool | None = None
