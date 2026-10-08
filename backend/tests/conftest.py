from __future__ import annotations

import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.security import create_access_token, hash_password
from app.api.deps import get_db
from app.database.base import Base
from app.main import app
from app.models import Preference, User

# In-memory SQLite for async tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture(autouse=True)
async def create_test_tables():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture()
async def db() -> AsyncGenerator[AsyncSession, None]:
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture()
async def client(db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture()
async def test_user(db: AsyncSession) -> User:
    user = User(
        email="test@brewdrift.com",
        password_hash=hash_password("testpassword123"),
        display_name="Test User",
        username="testuser",
    )
    db.add(user)
    await db.flush()
    pref = Preference(user_id=user.id)
    db.add(pref)
    await db.commit()
    await db.refresh(user)
    return user


@pytest_asyncio.fixture()
async def test_user2(db: AsyncSession) -> User:
    user = User(
        email="test2@brewdrift.com",
        password_hash=hash_password("testpassword123"),
        display_name="Test User 2",
        username="testuser2",
    )
    db.add(user)
    await db.flush()
    pref = Preference(user_id=user.id)
    db.add(pref)
    await db.commit()
    await db.refresh(user)
    return user


@pytest.fixture()
def auth_headers(test_user: User) -> dict[str, str]:
    token = create_access_token({"sub": test_user.id})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def auth_headers2(test_user2: User) -> dict[str, str]:
    token = create_access_token({"sub": test_user2.id})
    return {"Authorization": f"Bearer {token}"}
