import pandas as pd
from typing import List

my_path = "data_migration/data/ingreso_joyas_acero.xlsx"


def get_sheet_names(file_path: str) -> List[str]:
    # Read the excel file
    xls = pd.ExcelFile(file_path)
    # Get the name of all the sheets
    sheet_names = xls.sheet_names
    return sheet_names


sheet_names = get_sheet_names(my_path)

dataframes = []
for sheet_name in sheet_names:
    print(f"Sheet Name: {sheet_name}")
    df = pd.read_excel(my_path, sheet_name=sheet_name)
    df["source"] = sheet_name
    dataframes.append(df)
    print(f"Shape: {df.shape}")
    print(f"Column Names: {df.columns}\n")

all = pd.concat(dataframes)
all[all.pvp.isnull()][["codigo", "source"]]  # pulseras varios no tiene costo ni pvp


# insert records in all dataframe into a sqlite db named acero.db
import sqlite3

conn = sqlite3.connect("data_migration/data/acero.db")
all.to_sql("joyas", conn, if_exists="replace")
conn.close()

# read the data from the sqlite db
conn = sqlite3.connect("data_migration/data/acero.db")
query = """
    SELECT codigo, source, costo, pvp
    FROM joyas
    WHERE costo IS NULL OR pvp IS NULL
"""
df = pd.read_sql(query, conn)
conn.close()

print(df)
