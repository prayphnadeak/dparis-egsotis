import pandas as pd
import re
import math

def extract_coords(url):
    if not isinstance(url, str):
        return None
    # Look for !3d and !4d
    m = re.search(r'!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)', url)
    if m:
        return float(m.group(1)), float(m.group(2))
    
    # Fallback to @lat,lng
    m2 = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', url)
    if m2:
        return float(m2.group(1)), float(m2.group(2))
    
    # Fallback to /place/name/lat,lng
    m3 = re.search(r'/place/.*?/(-?\d+\.\d+),(-?\d+\.\d+)', url)
    if m3:
        return float(m3.group(1)), float(m3.group(2))
        
    return None

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # spherical earth radius in km
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

try:
    file_trans = r'c:\xampp\htdocs\dparis\backend\dparis_transportasi.xlsx'
    file_land = r'c:\xampp\htdocs\dparis\backend\dparis_landmark.xlsx'
    
    df_trans = pd.read_excel(file_trans)
    df_land = pd.read_excel(file_land)

    landmarks = {}
    for idx, row in df_land.iterrows():
        name = row['Nama Landmark']
        link = row['LINK']
        coords = extract_coords(link)
        if coords:
            landmarks[name] = coords
        else:
            print(f"[Warning] Failed to extract coords for Landmark: {name} from {link}")

    print(f"Extracted {len(landmarks)} landmarks.")

    updated_count = 0
    for idx, row in df_trans.iterrows():
        if row['No'] != 6 and row['Nama'] != 'DHARMA KARYA TRAVEL':
            continue
            
        link = row['Link']
        trans_coords = extract_coords(link)
        
        if not trans_coords:
            print(f"[Warning] Failed to extract coords for Transport: {row['Nama']} from {link}")
            continue
            
        for land_name, land_coords in landmarks.items():
            col_name = f"Jarak ke {land_name}"
            # Match the column if it exists or even if it needs to be added (though prompt says 'sesuai dengan kolom landmark yang tampil di dalamnya')
            if col_name in df_trans.columns:
                dist = haversine(trans_coords[0], trans_coords[1], land_coords[0], land_coords[1])
                df_trans.at[idx, col_name] = round(dist, 2)
                updated_count += 1
                
    print(f"Calculated and updated {updated_count} distance cells.")
    
    # Save back to excel
    df_trans.to_excel(file_trans, index=False)
    print("Saved dparis_transportasi.xlsx successfully.")
    
except Exception as e:
    import traceback
    traceback.print_exc()
    print("Error:", e)
