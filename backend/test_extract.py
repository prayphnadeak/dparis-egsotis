import pandas as pd
import re

files = [
    'dparis_wisata.xlsx',
    'dparis_kuliner.xlsx',
    'dparis_oleholeh.xlsx',
    'dparis_akomodasi.xlsx',
    'dparis_landmark.xlsx'
]

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
        
    # Pattern 4: query=lat,lon (sometimes used)
    match4 = re.search(r'query=(-?\d+\.\d+),(-?\d+\.\d+)', url)
    if match4:
        return float(match4.group(1)), float(match4.group(2))
        
    # Pattern 5: ll=lat,lon
    match5 = re.search(r'll=(-?\d+\.\d+),(-?\d+\.\d+)', url)
    if match5:
        return float(match5.group(1)), float(match5.group(2))

    # Pattern for short links, skipping for now
    return None

for f in files:
    try:
        df = pd.read_excel(f'c:/xampp/htdocs/dparis/backend/{f}')
        link_col = 'LINK' if 'LINK' in df.columns else 'Link'
        
        missing_coords = 0
        total = len(df)
        
        for idx, row in df.iterrows():
            url = row[link_col]
            coords = extract_coords(url)
            if not coords:
                missing_coords += 1
                
        print(f"{f}: {missing_coords}/{total} missing coordinates")
        
    except Exception as e:
        print(f"Error {f}: {e}")
