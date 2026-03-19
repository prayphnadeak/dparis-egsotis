import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import engine
from app.models.tourism import TourismObject
TourismObject.__table__.drop(engine, checkfirst=True)
print("Dropped tourism_objects table")
