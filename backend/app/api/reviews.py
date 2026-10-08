from __future__ import annotations

from fastapi import APIRouter, Response, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.deps import CurrentUser, DbSession
from app.models.review import Review
from app.models.visit import Visit
from app.schemas.review import CreateReviewRequest, ReviewResponse, UpdateReviewRequest

router = APIRouter(tags=["reviews"])


def _check_visit_ownership(visit: Visit | None, user_id: str) -> Visit:
    if visit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visit not found")
    if visit.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your visit")
    return visit


@router.get("/visits/{visit_id}/review", response_model=ReviewResponse)
async def get_review_for_visit(
    visit_id: str, current_user: CurrentUser, db: DbSession
) -> Review:
    visit_result = await db.execute(
        select(Visit).where(Visit.id == visit_id)
    )
    _check_visit_ownership(visit_result.scalar_one_or_none(), current_user.id)

    result = await db.execute(
        select(Review)
        .where(Review.visited_place_id == visit_id)
        .options(selectinload(Review.photos))
    )
    review = result.scalar_one_or_none()
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return review


@router.post(
    "/visits/{visit_id}/review",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_review(
    visit_id: str,
    body: CreateReviewRequest,
    current_user: CurrentUser,
    db: DbSession,
) -> Review:
    visit_result = await db.execute(select(Visit).where(Visit.id == visit_id))
    _check_visit_ownership(visit_result.scalar_one_or_none(), current_user.id)

    # Check if review already exists
    existing = await db.execute(
        select(Review).where(Review.visited_place_id == visit_id)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Review already exists for this visit",
        )

    review = Review(
        user_id=current_user.id,
        visited_place_id=visit_id,
        personal_rating=body.personal_rating,
        experience_text=body.experience_text,
        personal_tags=body.personal_tags,
    )
    db.add(review)
    await db.commit()

    # Reload with photos
    result = await db.execute(
        select(Review)
        .where(Review.id == review.id)
        .options(selectinload(Review.photos))
    )
    return result.scalar_one()


@router.patch("/reviews/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: str,
    body: UpdateReviewRequest,
    current_user: CurrentUser,
    db: DbSession,
) -> Review:
    result = await db.execute(
        select(Review)
        .where(Review.id == review_id, Review.user_id == current_user.id)
        .options(selectinload(Review.photos))
    )
    review = result.scalar_one_or_none()
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    if body.personal_rating is not None:
        review.personal_rating = body.personal_rating
    if body.experience_text is not None:
        review.experience_text = body.experience_text
    if body.personal_tags is not None:
        review.personal_tags = body.personal_tags

    await db.commit()
    await db.refresh(review)
    result2 = await db.execute(
        select(Review).where(Review.id == review.id).options(selectinload(Review.photos))
    )
    return result2.scalar_one()


@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_review(
    review_id: str, current_user: CurrentUser, db: DbSession
) -> None:
    result = await db.execute(
        select(Review).where(Review.id == review_id, Review.user_id == current_user.id)
    )
    review = result.scalar_one_or_none()
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    await db.delete(review)
    await db.commit()


