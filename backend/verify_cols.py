import pandas as pd
import os

target_files = [
    'dparis_wisata.xlsx',
    'dparis_kuliner.xlsx',
    'dparis_oleholeh.xlsx',
    'dparis_akomodasi.xlsx'
]
base_path = 'c:/xampp/htdocs/dparis/backend/'

for f in target_files:
    file_path = os.path.join(base_path, f)
    try:
        df = pd.read_excel(file_path)
        print(f"--- {f} ---")
        # Identify columns that start with 'Jarak ke'
        dist_cols = [c for c in df.columns if c.startswith('Jarak ke')]
        if len(dist_cols) > 0:
            print(df[dist_cols].head(5))
        else:
            print("No distance columns found!")
    except Exception as e:
        print(f"Error reading {f}: {e}")
