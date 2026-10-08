from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class CreateCollectionRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=1000)


class UpdateCollectionRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=1000)


class CollectionItemRequest(BaseModel):
    provider: str = Field(default="google", max_length=50)
    provider_place_id: str = Field(min_length=1, max_length=255)


class CollectionItemResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    collection_id: str
    provider: str
    provider_place_id: str
    created_at: datetime


class CollectionResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    name: str
    description: str | None
    cover_photo_url: str | None
    item_count: int = 0
    created_at: datetime
    updated_at: datetime


class CollectionDetailResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    name: str
    description: str | None
    cover_photo_url: str | None
    items: list[CollectionItemResponse] = []
    created_at: datetime
    updated_at: datetime
