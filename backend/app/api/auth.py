from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_reset_token,
    hash_password,
    verify_password,
)
from app.database.session import get_db
from app.models.password_reset import PasswordReset
from app.models.preference import Preference
from app.models.user import User
from app.schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    MessageResponse,
    RefreshRequest,
    RegisterRequest,
    ResetPasswordRequest,
    TokenResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])

DbSession = Annotated[AsyncSession, Depends(get_db)]


def _make_token_response(user: User) -> TokenResponse:
    access = create_access_token({"sub": user.id})
    refresh = create_refresh_token({"sub": user.id})
    return TokenResponse(
        access_token=access,
        refresh_token=refresh,
        expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest, db: DbSession) -> TokenResponse:
    # Check email uniqueness
    existing_email = await db.execute(
        select(User).where(User.email == body.email.lower())
    )
    if existing_email.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Check username uniqueness
    existing_username = await db.execute(
        select(User).where(User.username == body.username.lower())
    )
    if existing_username.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken",
        )

    user = User(
        email=body.email.lower(),
        password_hash=hash_password(body.password),
        display_name=body.display_name,
        username=body.username.lower(),
    )
    db.add(user)
    await db.flush()

    # Create default preferences
    pref = Preference(user_id=user.id)
    db.add(pref)

    await db.commit()
    await db.refresh(user)
    logger.info("New user registered: %s", user.id)
    return _make_token_response(user)


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db: DbSession) -> TokenResponse:
    result = await db.execute(
        select(User).where(User.email == body.email.lower(), User.is_deleted == False)
    )
    user = result.scalar_one_or_none()

    if user is None or not verify_password(body.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated",
        )

    return _make_token_response(user)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(body: RefreshRequest, db: DbSession) -> TokenResponse:
    payload = decode_token(body.refresh_token)
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    user_id = payload.get("sub")
    result = await db.execute(
        select(User).where(User.id == user_id, User.is_deleted == False, User.is_active == True)
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return _make_token_response(user)


@router.post("/logout", response_model=MessageResponse)
async def logout() -> MessageResponse:
    # With short-lived JWTs, logout is client-side (delete token).
    # For server-side invalidation, a token blacklist (Redis) would be added.
    return MessageResponse(message="Logged out successfully. Please discard your tokens.")


@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(body: ForgotPasswordRequest, db: DbSession) -> MessageResponse:
    result = await db.execute(
        select(User).where(User.email == body.email.lower(), User.is_deleted == False)
    )
    user = result.scalar_one_or_none()

    # Always return the same message to avoid user enumeration
    generic_msg = (
        "If that email is registered, a password reset link has been sent."
    )

    if user is None:
        return MessageResponse(message=generic_msg)

    raw_token, token_hash = generate_reset_token()
    reset = PasswordReset(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
    )
    db.add(reset)
    await db.commit()

    if settings.FORGOT_PASSWORD_DEV_MODE:
        logger.warning(
            "[DEV MODE] Password reset token for %s: %s", user.email, raw_token
        )
        return MessageResponse(
            message=f"[DEV MODE] Reset token: {raw_token}  (expires in 1 hour)"
        )

    # Production: send email here
    logger.info("Password reset requested for user %s", user.id)
    return MessageResponse(message=generic_msg)


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(body: ResetPasswordRequest, db: DbSession) -> MessageResponse:
    from app.core.security import hash_token

    token_hash = hash_token(body.token)
    now = datetime.now(timezone.utc)

    result = await db.execute(
        select(PasswordReset).where(
            PasswordReset.token_hash == token_hash,
            PasswordReset.used_at == None,
            PasswordReset.expires_at > now,
        )
    )
    reset = result.scalar_one_or_none()
    if reset is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )

    user_result = await db.execute(select(User).where(User.id == reset.user_id))
    user = user_result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    user.password_hash = hash_password(body.new_password)
    reset.used_at = now
    await db.commit()

    return MessageResponse(message="Password reset successfully.")
