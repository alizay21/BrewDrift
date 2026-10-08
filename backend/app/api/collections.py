from __future__ import annotations

from fastapi import APIRouter, Response, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.deps import CurrentUser, DbSession
from app.models.collection import Collection
from app.models.collection_item import CollectionItem
from app.schemas.collection import (
    CollectionDetailResponse,
    CollectionItemRequest,
    CollectionItemResponse,
    CollectionResponse,
    CreateCollectionRequest,
    UpdateCollectionRequest,
)

router = APIRouter(prefix="/collections", tags=["collections"])


def _to_collection_response(col: Collection) -> CollectionResponse:
    return CollectionResponse(
        id=col.id,
        name=col.name,
        description=col.description,
        cover_photo_url=col.cover_photo_url,
        item_count=len(col.items),
        created_at=col.created_at,
        updated_at=col.updated_at,
    )


@router.get("/", response_model=list[CollectionResponse])
async def list_collections(current_user: CurrentUser, db: DbSession) -> list[CollectionResponse]:
    result = await db.execute(
        select(Collection)
        .where(Collection.user_id == current_user.id)
        .options(selectinload(Collection.items))
        .order_by(Collection.created_at.desc())
    )
    cols = result.scalars().all()
    return [_to_collection_response(c) for c in cols]


@router.post("/", response_model=CollectionResponse, status_code=status.HTTP_201_CREATED)
async def create_collection(
    body: CreateCollectionRequest, current_user: CurrentUser, db: DbSession
) -> CollectionResponse:
    col = Collection(
        user_id=current_user.id,
        name=body.name,
        description=body.description,
    )
    db.add(col)
    await db.commit()
    await db.refresh(col)

    result = await db.execute(
        select(Collection).where(Collection.id == col.id).options(selectinload(Collection.items))
    )
    col = result.scalar_one()
    return _to_collection_response(col)


@router.get("/{collection_id}", response_model=CollectionDetailResponse)
async def get_collection(
    collection_id: str, current_user: CurrentUser, db: DbSession
) -> Collection:
    result = await db.execute(
        select(Collection)
        .where(Collection.id == collection_id, Collection.user_id == current_user.id)
        .options(selectinload(Collection.items))
    )
    col = result.scalar_one_or_none()
    if col is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")
    return col


@router.patch("/{collection_id}", response_model=CollectionResponse)
async def update_collection(
    collection_id: str,
    body: UpdateCollectionRequest,
    current_user: CurrentUser,
    db: DbSession,
) -> CollectionResponse:
    result = await db.execute(
        select(Collection)
        .where(Collection.id == collection_id, Collection.user_id == current_user.id)
        .options(selectinload(Collection.items))
    )
    col = result.scalar_one_or_none()
    if col is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")

    if body.name is not None:
        col.name = body.name
    if body.description is not None:
        col.description = body.description

    await db.commit()
    await db.refresh(col)
    result2 = await db.execute(
        select(Collection).where(Collection.id == col.id).options(selectinload(Collection.items))
    )
    col = result2.scalar_one()
    return _to_collection_response(col)


@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_collection(
    collection_id: str, current_user: CurrentUser, db: DbSession
) -> None:
    result = await db.execute(
        select(Collection).where(
            Collection.id == collection_id, Collection.user_id == current_user.id
        )
    )
    col = result.scalar_one_or_none()
    if col is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")
    await db.delete(col)
    await db.commit()


@router.post(
    "/{collection_id}/items",
    response_model=CollectionItemResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_collection_item(
    collection_id: str,
    body: CollectionItemRequest,
    current_user: CurrentUser,
    db: DbSession,
) -> CollectionItem:
    col_result = await db.execute(
        select(Collection).where(
            Collection.id == collection_id, Collection.user_id == current_user.id
        )
    )
    if col_result.scalar_one_or_none() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")

    existing = await db.execute(
        select(CollectionItem).where(
            CollectionItem.collection_id == collection_id,
            CollectionItem.provider == body.provider,
            CollectionItem.provider_place_id == body.provider_place_id,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Place already in this collection",
        )

    item = CollectionItem(
        collection_id=collection_id,
        provider=body.provider,
        provider_place_id=body.provider_place_id,
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router.delete("/{collection_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def remove_collection_item(
    collection_id: str,
    item_id: str,
    current_user: CurrentUser,
    db: DbSession,
) -> None:
    col_result = await db.execute(
        select(Collection).where(
            Collection.id == collection_id, Collection.user_id == current_user.id
        )
    )
    if col_result.scalar_one_or_none() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")

    item_result = await db.execute(
        select(CollectionItem).where(
            CollectionItem.id == item_id,
            CollectionItem.collection_id == collection_id,
        )
    )
    item = item_result.scalar_one_or_none()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    await db.delete(item)
    await db.commit()


