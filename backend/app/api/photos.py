from __future__ import annotations

import math

from fastapi import APIRouter, Response, File, HTTPException, UploadFile, status
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.api.deps import CurrentUser, DbSession
from app.core.config import settings
from app.models.photo import Photo
from app.models.review import Review
from app.schemas.review import PhotoResponse
from app.services.storage_service import StorageService

router = APIRouter(tags=["photos"])

MAX_PHOTOS_PER_REVIEW = 5


@router.post(
    "/reviews/{review_id}/photos",
    response_model=PhotoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_photo(
    review_id: str,
    current_user: CurrentUser,
    db: DbSession,
    file: UploadFile = File(...),
) -> Photo:
    # Verify review ownership
    result = await db.execute(
        select(Review).where(
            Review.id == review_id,
            Review.user_id == current_user.id,
        )
    )
    review = result.scalar_one_or_none()
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    # Check photo count
    count_result = await db.execute(
        select(func.count()).where(Photo.review_id == review_id)
    )
    photo_count = count_result.scalar_one()
    if photo_count >= MAX_PHOTOS_PER_REVIEW:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Maximum {MAX_PHOTOS_PER_REVIEW} photos per review",
        )

    # Validate content-type header
    mime_type = file.content_type or "application/octet-stream"

    # Read file bytes
    file_bytes = await file.read()

    storage = StorageService()
    try:
        storage.validate_image(file_bytes, mime_type)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        )

    url = await storage.save_file(file_bytes, file.filename or "upload.jpg", mime_type)

    photo = Photo(
        review_id=review_id,
        storage_url=url,
        filename=file.filename or "upload.jpg",
        mime_type=mime_type,
        file_size_kb=math.ceil(len(file_bytes) / 1024),
    )
    db.add(photo)
    await db.commit()
    await db.refresh(photo)
    return photo


@router.delete("/photos/{photo_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_photo(
    photo_id: str, current_user: CurrentUser, db: DbSession
) -> None:
    result = await db.execute(
        select(Photo)
        .where(Photo.id == photo_id)
        .options(selectinload(Photo.review))
    )
    photo = result.scalar_one_or_none()
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")

    if photo.review.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your photo")

    storage = StorageService()
    await storage.delete_file(photo.storage_url)

    await db.delete(photo)
    await db.commit()


