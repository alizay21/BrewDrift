from __future__ import annotations

import math
from dataclasses import dataclass, field

from app.models.favorite import Favorite
from app.models.visit import Visit
from app.schemas.place import Place, PlaceLocation
from app.schemas.recommendation import (
    PlaceRecommendation,
    RecommendationRequest,
    VibeScore,
)

# Vibe keyword mapping: vibe_id -> keywords to look for in place data
VIBE_KEYWORDS: dict[str, list[str]] = {
    "cozy": ["cozy", "cosy", "intimate", "warm", "snug", "nook", "quiet", "peaceful"],
    "lively": ["lively", "vibrant", "bustling", "social", "busy", "energetic"],
    "bookish": ["book", "library", "literary", "read", "shelf", "chapter"],
    "artsy": ["art", "gallery", "creative", "craft", "design", "studio", "exhibit"],
    "hipster": ["specialty", "third-wave", "roastery", "pour-over", "single-origin", "artisan"],
    "study": ["wifi", "cowork", "focus", "quiet", "laptop", "work"],
    "social": ["social", "community", "commons", "meeting", "chat"],
    "romantic": ["velvet", "intimate", "candle", "dim", "serene", "evening"],
    "outdoorsy": ["garden", "outdoor", "terrace", "patio", "park", "nature"],
    "foodie": ["brunch", "menu", "pastry", "bakery", "sourdough", "farm-to"],
    "caffeinated": ["coffee", "espresso", "brew", "roast", "latte", "cappuccino"],
    "trendy": ["modern", "minimal", "contemporary", "sleek", "new", "fresh"],
}

VIBE_TYPES: dict[str, list[str]] = {
    "bookish": ["book_store", "library"],
    "artsy": ["art_gallery", "museum"],
    "caffeinated": ["cafe", "coffee_shop"],
    "foodie": ["bakery", "restaurant", "meal_takeaway"],
    "social": ["bar", "restaurant"],
    "romantic": ["bar"],
    "lively": ["bar", "night_club", "restaurant"],
}


@dataclass
class RecommendationWeights:
    vibe: float = 0.40
    preference: float = 0.20
    distance: float = 0.15
    rating: float = 0.15
    history: float = 0.10


def _haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(
        math.radians(lat2)
    ) * math.sin(dlng / 2) ** 2
    return R * 2 * math.asin(math.sqrt(a))


class RecommendationService:
    def __init__(self, weights: RecommendationWeights | None = None) -> None:
        self.weights = weights or RecommendationWeights()

    def score_vibe_match(
        self, place: Place, vibes: list[str]
    ) -> dict[str, VibeScore]:
        if not vibes:
            return {}

        # Build searchable text corpus from place data
        corpus = " ".join(
            filter(
                None,
                [
                    place.name.lower(),
                    (place.editorial_summary or "").lower(),
                    " ".join(place.types).lower(),
                    (place.address or "").lower(),
                ],
            )
        )

        scores: dict[str, VibeScore] = {}
        for vibe in vibes:
            vibe_id = vibe.lower()
            keywords = VIBE_KEYWORDS.get(vibe_id, [vibe_id])
            type_hints = VIBE_TYPES.get(vibe_id, [])
            evidence: list[str] = []
            keyword_hits = 0

            for kw in keywords:
                if kw in corpus:
                    keyword_hits += 1
                    if kw in place.name.lower():
                        evidence.append(f"Name suggests '{kw}'")
                    elif kw in (place.editorial_summary or "").lower():
                        evidence.append(f"Description mentions '{kw}'")

            type_hits = sum(1 for t in type_hints if t in place.types)
            if type_hits:
                evidence.append(f"Place type matches {vibe_id} category")

            raw_score = min(1.0, (keyword_hits * 0.25) + (type_hits * 0.35))

            if raw_score >= 0.70:
                confidence = "high"
            elif raw_score >= 0.40:
                confidence = "medium"
            else:
                confidence = "low"

            scores[vibe_id] = VibeScore(
                vibe_id=vibe_id,
                score=round(raw_score, 3),
                confidence=confidence,
                evidence=evidence[:4],
            )
        return scores

    def score_distance(
        self, place_location: PlaceLocation, user_lat: float, user_lng: float, max_radius_m: int
    ) -> float:
        dist_km = _haversine_km(
            user_lat, user_lng, place_location.lat, place_location.lng
        )
        max_km = max_radius_m / 1000.0
        if dist_km >= max_km:
            return 0.0
        return round(1.0 - (dist_km / max_km), 3)

    def score_rating(self, rating: float | None) -> float:
        if rating is None:
            return 0.3  # neutral
        return round(min(1.0, rating / 5.0), 3)

    def score_personal_history(
        self,
        place_id: str,
        provider: str,
        favorites: list[Favorite],
        visits: list[Visit],
    ) -> float:
        is_fav = any(
            f.provider_place_id == place_id and f.provider == provider for f in favorites
        )
        has_visit = any(
            v.provider_place_id == place_id and v.provider == provider for v in visits
        )
        score = 0.0
        if is_fav:
            score += 0.6
        if has_visit:
            score += 0.4
        return min(1.0, score)

    def filter_places(self, places: list[Place]) -> list[Place]:
        filtered = []
        for p in places:
            if not p.name or not p.location:
                continue
            if p.rating is not None and p.rating < 1.0:
                continue
            filtered.append(p)
        return filtered

    def score_place(
        self,
        place: Place,
        request: RecommendationRequest,
        user_favorites: list[Favorite],
        user_visits: list[Visit],
    ) -> PlaceRecommendation:
        w = self.weights
        vibe_scores = self.score_vibe_match(place, request.selected_vibes)

        # Average vibe score
        avg_vibe = (
            sum(v.score for v in vibe_scores.values()) / len(vibe_scores)
            if vibe_scores
            else 0.5
        )

        dist_score = self.score_distance(
            place.location, request.lat, request.lng, request.radius_m
        )
        rating_score = self.score_rating(place.rating)
        history_score = self.score_personal_history(
            place.place_id, "google", user_favorites, user_visits
        )

        # Preference: boost if matches min_rating filter
        pref_score = 0.5
        if request.filters.min_rating and place.rating:
            pref_score = 1.0 if place.rating >= request.filters.min_rating else 0.1

        overall = round(
            w.vibe * avg_vibe
            + w.preference * pref_score
            + w.distance * dist_score
            + w.rating * rating_score
            + w.history * history_score,
            4,
        )

        if overall >= 0.70:
            confidence = "high"
        elif overall >= 0.40:
            confidence = "medium"
        else:
            confidence = "low"

        evidence: list[str] = []
        if rating_score >= 0.8 and place.rating:
            evidence.append(f"Highly rated ({place.rating:.1f}★)")
        if dist_score >= 0.7:
            evidence.append("Close to your location")
        if history_score > 0:
            evidence.append("In your favorites or visited before")
        for vs in vibe_scores.values():
            evidence.extend(vs.evidence[:2])

        return PlaceRecommendation(
            place=place,
            vibe_scores=vibe_scores,
            overall_score=min(1.0, overall),
            confidence=confidence,
            evidence=list(dict.fromkeys(evidence))[:6],
        )

    def rank_recommendations(
        self,
        request: RecommendationRequest,
        places: list[Place],
        user_favorites: list[Favorite],
        user_visits: list[Visit],
    ) -> list[PlaceRecommendation]:
        filtered = self.filter_places(places)

        # Apply hard filters
        if request.filters.min_rating is not None:
            filtered = [
                p for p in filtered
                if p.rating is None or p.rating >= request.filters.min_rating
            ]
        if request.filters.open_now is True:
            filtered = [
                p for p in filtered
                if p.opening_hours and p.opening_hours.open_now is True
            ]

        recs = [
            self.score_place(p, request, user_favorites, user_visits)
            for p in filtered
        ]
        recs.sort(key=lambda r: r.overall_score, reverse=True)
        return recs
