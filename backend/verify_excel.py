import pandas as pd

try:
    df = pd.read_excel('dparis_akomodasi.xlsx')
    print("Columns:", df.columns.tolist())
    print("First 5 non-null distances:")
    print(df[['NAMA', 'JARAK KE GUNUNG DEMPO']].dropna().head(5))
except Exception as e:
    print("Error:", e)
