from __future__ import annotations

import hashlib
import io
import logging
import os
import uuid
from pathlib import Path

import aiofiles
from PIL import Image

from app.core.config import settings

logger = logging.getLogger(__name__)

ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


class StorageService:
    def __init__(self) -> None:
        self._base_path = Path(settings.LOCAL_STORAGE_PATH)
        self._base_path.mkdir(parents=True, exist_ok=True)

    def validate_image(self, file_bytes: bytes, mime_type: str) -> None:
        """Validate MIME type, extension, and image integrity. Raises ValueError on failure."""
        if mime_type not in ALLOWED_MIME_TYPES:
            raise ValueError(
                f"Unsupported MIME type '{mime_type}'. "
                f"Allowed: {', '.join(sorted(ALLOWED_MIME_TYPES))}"
            )
        if len(file_bytes) > settings.max_upload_bytes:
            raise ValueError(
                f"File exceeds maximum size of {settings.MAX_UPLOAD_SIZE_MB} MB."
            )
        try:
            img = Image.open(io.BytesIO(file_bytes))
            img.verify()
        except Exception as exc:
            raise ValueError(f"Invalid or corrupt image file: {exc}") from exc

    async def save_file(
        self, file_bytes: bytes, filename: str, mime_type: str
    ) -> str:
        """Persist file to local storage and return the public URL path."""
        # Generate a unique filename to avoid collisions
        ext = Path(filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            ext = ".jpg"
        unique_name = f"{uuid.uuid4().hex}{ext}"
        dest = self._base_path / unique_name

        async with aiofiles.open(dest, "wb") as fh:
            await fh.write(file_bytes)

        logger.info("Saved file: %s (%d bytes)", dest, len(file_bytes))
        return f"/uploads/{unique_name}"

    async def delete_file(self, url: str) -> bool:
        """Delete a file by its URL path. Returns True on success."""
        try:
            filename = url.split("/")[-1]
            dest = self._base_path / filename
            if dest.exists():
                dest.unlink()
                logger.info("Deleted file: %s", dest)
                return True
            return False
        except Exception as exc:
            logger.error("Failed to delete file %s: %s", url, exc)
            return False
