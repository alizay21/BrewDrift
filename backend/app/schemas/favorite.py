from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class CreateFavoriteRequest(BaseModel):
    provider: str = Field(default="google", max_length=50)
    provider_place_id: str = Field(min_length=1, max_length=255)


class FavoriteResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    user_id: str
    provider: str
    provider_place_id: str
    created_at: datetime
