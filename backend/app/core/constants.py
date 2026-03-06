"""Application-wide constants."""
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    OPERATOR = "operator"
    PUBLIC = "public"


class ComplaintStatus(str, Enum):
    PENDING = "pending"
    IN_PROCESS = "in_process"
    RESOLVED = "resolved"
    REJECTED = "rejected"


class AccommodationCategory(str, Enum):
    HOTEL_NON_BINTANG = "Hotel Non Bintang"
    HOTEL_BINTANG_1 = "Hotel Bintang 1"
    HOTEL_BINTANG_2 = "Hotel Bintang 2"
    HOTEL_BINTANG_3 = "Hotel Bintang 3"
    HOTEL_BINTANG_4 = "Hotel Bintang 4"
    HOTEL_BINTANG_5 = "Hotel Bintang 5"
    HOMESTAY = "Homestay"
    VILLA = "Villa"
    PENGINAPAN = "Penginapan"
    GUEST_HOUSE = "Guest House"


class TourismCategory(str, Enum):
    AIR_TERJUN = "Air Terjun"
    AGROWISATA = "Agrowisata"
    WISATA_ALAM = "Wisata Alam"
    WISATA_BUDAYA = "Wisata Budaya"
    PENDAKIAN = "Pendakian"
    WISATA_SEJARAH = "Wisata Sejarah"
    WISATA_RELIGI = "Wisata Religi"


class CulinaryCategory(str, Enum):
    KEDAI = "Kedai"
    CAFE = "Cafe"
    RESTORAN = "Restoran"
    WARUNG = "Warung"
    RUMAH_MAKAN = "Rumah Makan"


class ComplaintCategory(str, Enum):
    AKOMODASI = "Akomodasi"
    WISATA = "Wisata"
    KULINER = "Kuliner"
    INFRASTRUKTUR = "Infrastruktur"
    PELAYANAN = "Pelayanan"
    LAINNYA = "Lainnya"


# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# File upload
UPLOAD_SUBDIRS = {
    "accommodation": "accommodations",
    "tourism": "tourism",
    "culinary": "culinary",
    "infographic": "infographics",
    "complaint": "complaints",
}

# Pagar Alam bounding box (lat/lng)
PAGAR_ALAM_BOUNDS = {
    "min_lat": -4.20,
    "max_lat": -3.85,
    "min_lng": 103.10,
    "max_lng": 103.50,
}
