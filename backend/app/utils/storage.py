import os
from typing import Optional
from supabase import create_client, Client
from app.core.config import settings

def get_supabase_client() -> Optional[Client]:
    """Inisialisasi dan ambil client Supabase."""
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        return None
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def upload_file_to_supabase(file_content: bytes, file_name: str, folder: str = "uploads") -> Optional[str]:
    """
    Upload file ke Supabase Storage dan kembalikan URL publiknya.
    
    Args:
        file_content: Isi file dalam bentuk bytes.
        file_name: Nama file (sebaiknya sudah unik).
        folder: Folder tujuan di dalam bucket.
        
    Returns:
        URL publik file atau None jika gagal.
    """
    supabase = get_supabase_client()
    if not supabase:
        print("Supabase client tidak terkonfigurasi.")
        return None
        
    try:
        path_on_supa = f"{folder}/{file_name}"
        
        # Upload file (upsert=True agar bisa overwrite jika nama sama)
        res = supabase.storage.from_(settings.SUPABASE_BUCKET).upload(
            path=path_on_supa,
            file=file_content,
            file_options={"x-upsert": "true"}
        )
        
        # Ambil URL Publik
        public_url = supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(path_on_supa)
        return public_url
    except Exception as e:
        print(f"Gagal upload ke Supabase: {str(e)}")
        return None
