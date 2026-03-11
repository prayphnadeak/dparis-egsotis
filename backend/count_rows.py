import openpyxl
import os

files = [
    'dparis_akomodasi.xlsx',
    'dparis_kuliner.xlsx',
    'dparis_oleholeh.xlsx',
    'dparis_wisata.xlsx'
]

for f in files:
    path = os.path.join(os.getcwd(), f)
    if os.path.exists(path):
        wb = openpyxl.load_workbook(path)
        ws = wb.active
        count = 0
        for row in ws.iter_rows(min_row=2, values_only=True):
            if any(v is not None for v in row):
                count += 1
        print(f"{f}: {count} rows")
    else:
        print(f"{f}: NOT FOUND at {path}")
