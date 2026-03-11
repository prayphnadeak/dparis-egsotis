import os
import sys

# Add root backend to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.tourism import TourismObject
from app.models.culinary import CulinaryPlace
from app.models.souvenir import SouvenirShop
from app.models.accommodation import Accommodation

def check_db():
    db = SessionLocal()
    try:
        print(f"Tourism: {db.query(TourismObject).count()}")
        print(f"Culinary: {db.query(CulinaryPlace).count()}")
        print(f"Souvenirs: {db.query(SouvenirShop).count()}")
        print(f"Accommodations: {db.query(Accommodation).count()}")
    finally:
        db.close()

if __name__ == "__main__":
    check_db()
