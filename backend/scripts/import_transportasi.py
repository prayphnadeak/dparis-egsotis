import sys
import os
import pandas as pd

# Add backend directory to sys.path so 'app' can be imported
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, backend_dir)

from app.db.session import SessionLocal, engine
from app.models.base import Base
# ensure the model is imported before create_all
from app.models.transportation import Transportation

def parse_bool(val):
    if pd.isna(val):
        return False
    return str(val).strip().lower() == 'ada'

def import_transportation():
    # CREATE TABLE
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    df = pd.read_excel('dparis_transportasi.xlsx')
    
    # Process rows
    for idx, row in df.iterrows():
        # Check if already exists? (Maybe not needed if table is fresh, but safe to check)
        name = row['Nama']
        existing = db.query(Transportation).filter(Transportation.name == name).first()
        if existing:
            continue
        
        rating = None
        if not pd.isna(row['RATING']):
            rating = float(row['RATING'])
            
        kontak = str(row['KONTAK']).strip() if pd.notna(row['KONTAK']) else None
        if kontak and kontak.endswith('.0'):
            kontak = kontak[:-2]
        
        # Mapping distance columns carefully
        def get_dist(col_name):
            if col_name in df.columns and pd.notna(row[col_name]):
                return float(row[col_name])
            return None
            
        trans = Transportation(
            name=name,
            category=row['MODA TRANSPORTASI'],
            rating=rating,
            route_palembang=parse_bool(row['PAGAR ALAM - PALEMBANG']),
            route_bengkulu=parse_bool(row['PAGAR ALAM - BENGKULU']),
            route_lampung=parse_bool(row['PAGAR ALAM - LAMPUNG']),
            route_jabodetabek=parse_bool(row['PAGAR ALAM - JABODETABEK']),
            route_jawa=parse_bool(row['PAGAR ALAM - JAWA (SANUTRA)']),
            phone=kontak,
            maps_link=row['Link'],
            dist_gunung_dempo=get_dist('Jarak ke GUNUNG DEMPO'),
            dist_pasar_dempo_permai=get_dist('Jarak ke PASAR DEMPO PERMAI'),
            dist_bandara_atung_bungsu=get_dist('Jarak ke BANDARA ATUNG BUNGSU'),
            dist_rsud_besemah=get_dist('Jarak ke RSUD BESEMAH'),
            dist_spbu_air_perikan=get_dist('Jarak ke SPBU AIR PERIKAN'),
            dist_spbu_simpang_manna=get_dist('Jarak ke SPBU SIMPANG MANNA'),
            dist_spbu_pengandonan=get_dist('Jarak ke SPBU PENGANDONAN'),
            dist_spbu_karang_dalo=get_dist('Jarak ke SPBU KARANG DALO'),
            is_active=True
        )
        db.add(trans)
        
    db.commit()
    print("Database imported successfully. Rows count:", db.query(Transportation).count())

if __name__ == "__main__":
    import_transportation()
