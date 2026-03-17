import pandas as pd
import re
import math

def haversine(lat1, lon1, lat2, lon2):
    # Radius of earth in meters
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def extract_coords(url):
    if not isinstance(url, str):
        return None, None
    
    # Try finding !3d<lat>!4d<lon>
    # Note: it can be !3d-4.0158333!4d103.1283333
    match_3d4d = re.search(r'!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)', url)
    if match_3d4d:
        return float(match_3d4d.group(1)), float(match_3d4d.group(2))
    
    # Try finding /@<lat>,<lon>
    match_at = re.search(r'/@(-?\d+\.\d+),(-?\d+\.\d+)', url)
    if match_at:
        return float(match_at.group(1)), float(match_at.group(2))
    
    return None, None

df = pd.read_excel('dparis_akomodasi.xlsx')

success = 0
failed = 0
gunung_dempo = (-4.0158333, 103.1283333)

distances = []
for i, row in df.iterrows():
    link = row['LINK']
    lat, lon = extract_coords(link)
    if lat is not None and lon is not None:
        dist = haversine(lat, lon, gunung_dempo[0], gunung_dempo[1])
        distances.append(round(dist))
        success += 1
    else:
        distances.append(None)
        failed += 1
        print(f"Failed to extract for row {i}: {link}")

print(f"Extraction success: {success}, failed: {failed}")
if failed == 0:
    df['JARAK KE GUNUNG DEMPO'] = distances
    print("Writing distances to new file dparis_akomodasi_new.xlsx...")
    df.to_excel('dparis_akomodasi_new.xlsx', index=False)
    print("Done!")
