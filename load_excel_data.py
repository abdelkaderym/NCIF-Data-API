import sqlite3
import pandas as pd

db_name = "ncif_data.db"
excel_file = "20241125 Case Study for Position SE_Data.xlsx"

conn = sqlite3.connect(db_name)
cursor = conn.cursor()

def load_sheet_to_table(sheet_name, table_name):
    try:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"Successfully loaded {table_name} from sheet '{sheet_name}' into SQLite database.")
    except Exception as e:
        print(f"Error loading {table_name}: {e}")

load_sheet_to_table("AirQuality_EPA_IL", "epa_data")  
load_sheet_to_table("SOD_IL_2024", "sod_data")  
load_sheet_to_table("NCUA_IL_Q2_2024", "credit_union_data")  
print("Tables in the database:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

conn.close()
