import pandas as pd

df = pd.read_excel('dparis_akomodasi.xlsx')
for i, link in enumerate(df['LINK'].head(10)):
    print(f"Row {i}: {link}")
