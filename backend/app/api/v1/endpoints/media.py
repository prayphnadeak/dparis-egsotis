"""Media upload endpoints."""
from fastapi import APIRouter, Depends, UploadFile, File, Form
from app.utils.file_upload import save_upload
from app.core.dependencies import get_current_admin
from app.models.user import User

router = APIRouter()

@router.post("/upload", summary="Upload media file (admin)")
async def upload_media(
    file: UploadFile = File(...),
    entity: str = Form("misc"),
    _: User = Depends(get_current_admin)
):
    """
    Mengunggah file ke storage (Supabase atau Lokal).
    'entity' menentukan folder tujuan: 'tourism', 'accommodations', 'infographics', dll.
    """
    url = await save_upload(file, entity)
    return {"url": url}
