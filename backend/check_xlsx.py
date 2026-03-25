import pandas as pd

try:
    df_trans = pd.read_excel(r'c:\xampp\htdocs\dparis\backend\dparis_transportasi.xlsx')
    df_land = pd.read_excel(r'c:\xampp\htdocs\dparis\backend\dparis_landmark.xlsx')

    print("Transportasi Columns:")
    print(df_trans.columns.tolist())
    print()
    print("Transportasi Data (First 3):")
    for index, row in df_trans.head(3).iterrows():
        print(row.to_dict())

    print("\nLandmark Columns:")
    print(df_land.columns.tolist())
    print()
    print("Landmark Data (First 3):")
    for index, row in df_land.head(3).iterrows():
        print(row.to_dict())

except Exception as e:
    print("Error:", e)
