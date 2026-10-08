from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    email: EmailStr
    display_name: str
    username: str
    bio: str | None = None
    profile_photo_url: str | None = None
    created_at: datetime


class UpdateUserRequest(BaseModel):
    display_name: str | None = Field(default=None, min_length=1, max_length=100)
    username: str | None = Field(
        default=None, min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$"
    )
    bio: str | None = Field(default=None, max_length=500)
