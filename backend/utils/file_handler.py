"""
File Handler - Validates and stores uploaded files.
"""

import os
import shutil
from pathlib import Path
from typing import Tuple, Optional

from fastapi import UploadFile, HTTPException, status
from backend.config import settings
from backend.utils.helpers import generate_unique_filename


class FileHandler:
    """Handles file upload validation and storage."""

    UPLOAD_DIR = settings.UPLOAD_DIR

    @classmethod
    def validate_file(cls, file: UploadFile) -> Tuple[str, int]:
        """
        Validate uploaded file (type and size).
        Returns (extension, file_size).
        Raises HTTPException if invalid.
        """
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No filename provided.",
            )

        # Check extension
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type '{ext}' not allowed. Accepted: {settings.ALLOWED_EXTENSIONS}",
            )

        # Check file size (read content to determine size)
        content = file.file.read()
        file_size = len(content)
        file.file.seek(0)  # Reset for later reading

        max_size = settings.MAX_FILE_SIZE_MB * 1024 * 1024
        if file_size > max_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Max size: {settings.MAX_FILE_SIZE_MB}MB",
            )

        if file_size == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File is empty.",
            )

        return ext, file_size

    @classmethod
    async def save_file(cls, file: UploadFile, user_id: int) -> Tuple[str, str, int]:
        """
        Save uploaded file to disk.
        Returns (unique_filename, file_path, file_size).
        """
        ext, file_size = cls.validate_file(file)

        # Create user-specific upload directory
        user_dir = cls.UPLOAD_DIR / str(user_id)
        user_dir.mkdir(parents=True, exist_ok=True)

        # Generate unique filename
        unique_filename = generate_unique_filename(file.filename)
        file_path = user_dir / unique_filename

        # Save file
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        return unique_filename, str(file_path), file_size

    @classmethod
    def delete_file(cls, file_path: str) -> bool:
        """Delete a file from disk."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception:
            return False

    @classmethod
    def get_file_path(cls, file_path: str) -> Optional[str]:
        """Verify file exists and return its path."""
        if os.path.exists(file_path):
            return file_path
        return None
