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
