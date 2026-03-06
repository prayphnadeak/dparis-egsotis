import sys
import os
from sqlalchemy import text
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.db.session import engine
with engine.connect() as conn:
    print("Accommodations:")
    for row in conn.execute(text('SELECT id, name, is_active FROM accommodations LIMIT 5')):
        print(row)
    print("Tourism:")
    for row in conn.execute(text('SELECT id, name, is_active FROM tourism_objects LIMIT 5')):
        print(row)
    print("Culinary:")
    for row in conn.execute(text('SELECT id, name, is_active FROM culinary_places LIMIT 5')):
        print(row)
    print("Souvenir:")
    for row in conn.execute(text('SELECT id, name, is_active FROM souvenir_shops LIMIT 5')):
        print(row)
