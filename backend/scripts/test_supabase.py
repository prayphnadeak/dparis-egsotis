import sys
import os
import asyncio

# Menambahkan direktori root proyek ke sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Mocking settings untuk testing jika .env belum terisi lengkap di lokal
from app.core.config import settings
from app.utils.storage import upload_file_to_supabase

# Set manual untuk testing (Gunakan data dari user)
settings.SUPABASE_URL = "https://rqrwaxehvhryehgrrssh.supabase.co"
# Ambil dari env variable untuk keamanan
settings.SUPABASE_KEY = os.getenv("SUPABASE_KEY", "MASUKKAN_KEY_DI_SINI")
settings.SUPABASE_BUCKET = "dparis"

def test_upload():
    print("--- Memulai Test Upload Supabase Storage ---")
    
    test_content = b"Hello D'Paris! Ini adalah file test untuk Supabase Storage."
    test_filename = "test_connection.txt"
    
    print(f"Mencoba upload {test_filename} ke bucket '{settings.SUPABASE_BUCKET}'...")
    
    url = upload_file_to_supabase(test_content, test_filename, folder="test")
    
    if url:
        print(f"SUCCESS! File berhasil di-upload.")
        print(f"URL Publik: {url}")
    else:
        print("FAILED! Gagal upload. Pastikan:")
        print("1. Nama bucket 'dparis' sudah dibuat di Dashboard Supabase.")
        print("2. Bucket tersebut disetel sebagai 'Public'.")
        print("3. API Key memiliki izin untuk menulis ke bucket (RLS/Policy).")

if __name__ == "__main__":
    test_upload()
