import os
import uuid
from pathlib import Path
import aiofiles
from fastapi import HTTPException, UploadFile
from app.core.config import settings
from app.core.constants import UPLOAD_SUBDIRS
from app.utils.storage import upload_file_to_supabase


async def save_upload(file: UploadFile, entity: str) -> str:
    """
    Save an uploaded file.
    Gunakan Supabase jika dikonfigurasi, jika tidak gunakan local storage.
    """
    if file.content_type not in settings.allowed_image_types_list:
        raise HTTPException(status_code=400, detail=f"Tipe file tidak didukung: {file.content_type}")

    content = await file.read()
    if len(content) > settings.max_upload_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"Ukuran file melebihi batas {settings.MAX_UPLOAD_SIZE_MB}MB",
        )

    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else "jpg"
    filename = f"{uuid.uuid4().hex}.{ext}"
    subdir = UPLOAD_SUBDIRS.get(entity, "misc")

    # JALUR SUPABASE (Prioritas)
    if settings.SUPABASE_URL and settings.SUPABASE_KEY:
        url = upload_file_to_supabase(content, filename, folder=subdir)
        if url:
            return url

    # JALUR LOKAL (Fallback atau jika Supabase tidak dikonfigurasi)
    target_dir = Path(settings.UPLOAD_DIR) / subdir
    target_dir.mkdir(parents=True, exist_ok=True)
    filepath = target_dir / filename

    async with aiofiles.open(filepath, "wb") as f:
        await f.write(content)

    return f"/static/uploads/{subdir}/{filename}"


def delete_file(url: str) -> None:
    """Delete a previously uploaded file by its URL path (Local only)."""
    if not url or url.startswith("http"): # Skip cloud URLs
        return
    relative = url.lstrip("/")
    path = Path(relative)
    if path.exists():
        path.unlink(missing_ok=True)
