from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class PhotoResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    storage_url: str
    filename: str
    mime_type: str
    file_size_kb: int
    created_at: datetime


class CreateReviewRequest(BaseModel):
    personal_rating: float | None = Field(default=None, ge=0.0, le=5.0)
    experience_text: str | None = Field(default=None, max_length=5000)
    personal_tags: list[str] = []


class UpdateReviewRequest(BaseModel):
    personal_rating: float | None = Field(default=None, ge=0.0, le=5.0)
    experience_text: str | None = Field(default=None, max_length=5000)
    personal_tags: list[str] | None = None


class ReviewResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    visited_place_id: str
    personal_rating: float | None
    experience_text: str | None
    personal_tags: list[str]
    photos: list[PhotoResponse] = []
    created_at: datetime
    updated_at: datetime
