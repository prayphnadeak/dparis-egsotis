"""Script to seed the database with sample data for testing."""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import SessionLocal
from app.db.init_db import init_db
from app.models.accommodation import Accommodation
from app.models.tourism import TourismObject
from app.models.culinary import CulinaryPlace
from app.models.infographic import Infographic
import asyncio


ACCOMMODATIONS = [
    {"name": "HOTEL A", "category": "Hotel Non Bintang", "total_rooms": 20, "phone": "0812345678910",
     "hot_water": True, "tv_cable": True, "bed": True, "free_wifi": True, "meeting_room": True,
     "latitude": -4.0217, "longitude": 103.2540},
    {"name": "HOTEL B", "category": "Hotel Bintang 2", "total_rooms": 35, "phone": "0813456789012",
     "hot_water": True, "tv_cable": True, "bed": True, "free_wifi": True, "restaurant": True, "gym": True, "meeting_room": True,
     "latitude": -4.0250, "longitude": 103.2560},
    {"name": "HOMESTAY A", "category": "Homestay", "total_rooms": 8, "phone": "0815678901234",
     "hot_water": True, "bed": True, "free_wifi": True,
     "latitude": -4.0190, "longitude": 103.2510},
    {"name": "VILLA A", "category": "Villa", "total_rooms": 5, "phone": "0817890123456",
     "hot_water": True, "tv_cable": True, "bed": True, "free_wifi": True, "swimming_pool": True,
     "latitude": -4.0150, "longitude": 103.2490},
]

TOURISM = [
    {"name": "AIR TERJUN A", "category": "Air Terjun", "description": "Air terjun indah di kawasan Dempo.", "latitude": -4.0150, "longitude": 103.2350},
    {"name": "KEBUN TEH DEMPO", "category": "Agrowisata", "description": "Pemandangan kebun teh hijau yang luas.", "latitude": -4.0080, "longitude": 103.2200},
    {"name": "GUNUNG DEMPO", "category": "Pendakian", "description": "Gunung berapi aktif, 3.173 mdpl.", "latitude": -4.0050, "longitude": 103.1280},
    {"name": "BATU GAJAH", "category": "Wisata Budaya", "description": "Megalitik peninggalan Besemah Kuno.", "latitude": -4.0300, "longitude": 103.2600},
]

CULINARY = [
    {"name": "KEDAI A", "category": "Kedai", "opening_hours": "07.00-21.00", "phone": "081234567890", "latitude": -4.0220, "longitude": 103.2540},
    {"name": "CAFE A", "category": "Cafe", "opening_hours": "09.00-22.00", "phone": "081456789012", "latitude": -4.0200, "longitude": 103.2520},
    {"name": "CAFE B", "category": "Cafe", "opening_hours": "10.00-23.00", "phone": "081567890123", "latitude": -4.0210, "longitude": 103.2530},
    {"name": "RESTO", "category": "Restoran", "opening_hours": "11.00-21.00", "phone": "081789012345", "latitude": -4.0240, "longitude": 103.2560},
]

INFOGRAPHICS = [
    {"title": "Statistik Pariwisata Kota Pagar Alam 2024", "year": 2024, "description": "Ringkasan data kunjungan wisatawan 2024."},
    {"title": "Kunjungan Wisatawan 2023", "year": 2023, "description": "Data kunjungan di semua destinasi wisata."},
    {"title": "Akomodasi Kota Pagar Alam", "year": 2023, "description": "Direktori hotel, homestay, dan villa."},
]


def run():
    asyncio.run(init_db())
    db = SessionLocal()
    try:
        # Clear existing
        for cls in [Accommodation, TourismObject, CulinaryPlace, Infographic]:
            db.query(cls).delete()
        db.commit()

        for data in ACCOMMODATIONS:
            db.add(Accommodation(**data))
        for data in TOURISM:
            db.add(TourismObject(**data))
        for data in CULINARY:
            db.add(CulinaryPlace(**data))
        for data in INFOGRAPHICS:
            db.add(Infographic(**data))

        db.commit()
        print("✅ Sample data berhasil ditambahkan!")
    finally:
        db.close()


if __name__ == "__main__":
    run()
