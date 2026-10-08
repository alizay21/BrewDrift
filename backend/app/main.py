from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api import auth, collections, favorites, photos, places, recommendations, reviews, users, visits
from app.core.config import settings
from app.database.session import create_tables

logging.basicConfig(
    level=logging.DEBUG if not settings.is_production else logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Starting Brewdrift API (env=%s)", settings.ENVIRONMENT)
    await create_tables()
    logger.info("Database tables verified/created")
    yield
    logger.info("Shutting down Brewdrift API")


app = FastAPI(
    title="Brewdrift API",
    description="Backend for the Brewdrift cafe-discovery app",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
)

# ── CORS ────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Static files (uploaded images) ──────────────────────────────
import os as _os
_os.makedirs(settings.LOCAL_STORAGE_PATH, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.LOCAL_STORAGE_PATH), name="uploads")

# ── Routers ─────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(places.router)
app.include_router(recommendations.router)
app.include_router(favorites.router)
app.include_router(visits.router)
app.include_router(reviews.router)
app.include_router(photos.router)
app.include_router(collections.router)


# ── Exception handlers ──────────────────────────────────────────
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("Unhandled exception on %s %s: %s", request.method, request.url, exc, exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred. Please try again later."},
    )


# ── Health check ────────────────────────────────────────────────
@app.get("/health", tags=["health"])
async def health_check() -> dict:
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
        "use_mock_places": settings.USE_MOCK_PLACES,
    }
