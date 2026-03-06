import sys
import os

# Menambahkan direktori backend ke sys.path agar package 'app' bisa diimport
# Struktur:
# / (root)
# ├── api/index.py
# └── backend/app/
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.main import app
from mangum import Mangum

# Handler untuk Vercel Serverless Functions
handler = Mangum(app)
