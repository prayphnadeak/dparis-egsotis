import pandas as pd

files = [
    'dparis_wisata.xlsx',
    'dparis_kuliner.xlsx',
    'dparis_oleholeh.xlsx',
    'dparis_akomodasi.xlsx',
    'dparis_landmark.xlsx'
]

for f in files:
    try:
        df = pd.read_excel(f'c:/xampp/htdocs/dparis/backend/{f}')
        print(f"--- {f} ---")
        print(df.columns.tolist())
    except Exception as e:
        print(f"Error reading {f}: {e}")
