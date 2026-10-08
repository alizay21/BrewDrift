"""
Generator script - Batch 3: Pydantic schemas
"""
import os


def write(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Written: {path}")


write("app/schemas/auth.py", """\
from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    display_name: str = Field(min_length=1, max_length=100)
    username: str = Field(min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshRequest(BaseModel):
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


class MessageResponse(BaseModel):
    message: str
""")

write("app/schemas/user.py", """\
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
""")

write("app/schemas/preference.py", """\
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
""")

write("app/schemas/place.py", """\
from __future__ import annotations

from pydantic import BaseModel, Field


class PlaceLocation(BaseModel):
    lat: float
    lng: float


class PlacePhoto(BaseModel):
    photo_reference: str
    url: str | None = None
    width: int = 0
    height: int = 0
    attributions: list[str] = []


class PlaceOpeningHoursPeriodTime(BaseModel):
    day: int
    hour: int
    minute: int


class PlaceOpeningHoursPeriod(BaseModel):
    open: PlaceOpeningHoursPeriodTime | None = None
    close: PlaceOpeningHoursPeriodTime | None = None


class PlaceOpeningHours(BaseModel):
    open_now: bool | None = None
    periods: list[PlaceOpeningHoursPeriod] | None = None
    weekday_descriptions: list[str] | None = None


class Place(BaseModel):
    place_id: str
    name: str
    location: PlaceLocation
    address: str | None = None
    rating: float | None = None
    rating_count: int | None = None
    photos: list[PlacePhoto] = []
    opening_hours: PlaceOpeningHours | None = None
    types: list[str] = []
    price_level: str | None = None
    phone: str | None = None
    website: str | None = None
    editorial_summary: str | None = None


class NearbyPlacesRequest(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lng: float = Field(ge=-180, le=180)
    radius_m: int = Field(default=1500, ge=1, le=50000)
    max_results: int = Field(default=20, ge=1, le=50)


class NearbyPlacesResponse(BaseModel):
    places: list[Place]
    total: int


class SearchPlacesRequest(BaseModel):
    query: str = Field(min_length=1, max_length=200)
    lat: float | None = Field(default=None, ge=-90, le=90)
    lng: float | None = Field(default=None, ge=-180, le=180)


class SearchPlacesResponse(BaseModel):
    places: list[Place]
    total: int
""")

write("app/schemas/recommendation.py", """\
from __future__ import annotations

from pydantic import BaseModel, Field

from app.schemas.place import Place


class RecommendationFilters(BaseModel):
    min_rating: float | None = Field(default=None, ge=0.0, le=5.0)
    open_now: bool | None = None
    max_price_level: int | None = Field(default=None, ge=1, le=4)
    types: list[str] | None = None


class RecommendationRequest(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lng: float = Field(ge=-180, le=180)
    selected_vibes: list[str] = []
    mood_text: str | None = Field(default=None, max_length=300)
    radius_m: int = Field(default=2000, ge=100, le=50000)
    filters: RecommendationFilters = RecommendationFilters()


class VibeScore(BaseModel):
    vibe_id: str
    score: float = Field(ge=0.0, le=1.0)
    confidence: str  # 'high', 'medium', 'low'
    evidence: list[str] = []


class PlaceRecommendation(BaseModel):
    place: Place
    vibe_scores: dict[str, VibeScore] = {}
    overall_score: float = Field(ge=0.0, le=1.0)
    confidence: str
    evidence: list[str] = []


class RecommendationResponse(BaseModel):
    recommendations: list[PlaceRecommendation]
    total: int
""")

write("app/schemas/favorite.py", """\
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
""")

write("app/schemas/visit.py", """\
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
""")

write("app/schemas/review.py", """\
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
""")

write("app/schemas/collection.py", """\
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
""")

print("\nBatch 3 complete: all schemas written")
