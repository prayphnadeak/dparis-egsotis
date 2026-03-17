import pandas as pd
import re
import math
import os

target_files = [
    'dparis_wisata.xlsx',
    'dparis_kuliner.xlsx',
    'dparis_oleholeh.xlsx',
    'dparis_akomodasi.xlsx'
]

landmark_file = 'dparis_landmark.xlsx'
base_path = 'c:/xampp/htdocs/dparis/backend/'

def extract_coords(url):
    if not isinstance(url, str):
        return None
    # Pattern 1: @lat,lon
    match1 = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', url)
    if match1:
        return float(match1.group(1)), float(match1.group(2))
    # Pattern 2: !3dlat!4dlon
    match2 = re.search(r'!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)', url)
    if match2:
        return float(match2.group(1)), float(match2.group(2))
    # Pattern 3: q=lat,lon
    match3 = re.search(r'q=(-?\d+\.\d+),(-?\d+\.\d+)', url)
    if match3:
        return float(match3.group(1)), float(match3.group(2))
    # Pattern 4: query=lat,lon
    match4 = re.search(r'query=(-?\d+\.\d+),(-?\d+\.\d+)', url)
    if match4:
        return float(match4.group(1)), float(match4.group(2))
    # Pattern 5: ll=lat,lon
    match5 = re.search(r'll=(-?\d+\.\d+),(-?\d+\.\d+)', url)
    if match5:
        return float(match5.group(1)), float(match5.group(2))
    return None

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0 # Earth radius in kilometers
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# 1. Read Landmarks
df_landmark = pd.read_excel(os.path.join(base_path, landmark_file))
landmarks = []
for idx, row in df_landmark.iterrows():
    name = row['Nama Landmark']
    link = row['LINK']
    coords = extract_coords(link)
    if coords:
        landmarks.append({'name': name, 'coords': coords})
    else:
        print(f"Warning: Could not extract coordinates for landmark {name}")

# 2. Process each target file
for f in target_files:
    file_path = os.path.join(base_path, f)
    try:
        df = pd.read_excel(file_path)
        link_col = 'LINK' if 'LINK' in df.columns else 'Link'
        
        # Add new columns for landmarks
        for landmark in landmarks:
            lm_name = landmark['name']
            lm_coords = landmark['coords']
            col_name = f"Jarak ke {lm_name}"
            
            distances = []
            for _, row in df.iterrows():
                url = row[link_col]
                row_coords = extract_coords(url)
                if row_coords:
                    dist = haversine(row_coords[0], row_coords[1], lm_coords[0], lm_coords[1])
                    distances.append(round(dist, 2))
                else:
                    distances.append(None)
            
            df[col_name] = distances
            
        # Save back to excel
        df.to_excel(file_path, index=False)
        print(f"Successfully updated {f}")
        
    except Exception as e:
        print(f"Error processing {f}: {e}")

print("Processing finished.")
