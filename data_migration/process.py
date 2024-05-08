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
    dataframes.append(df)
    print(f"Shape: {df.shape}")
    print(f"Column Names: {df.columns}\n")

pd.concat(dataframes).columns

## To do, clean column names until we have a unified df