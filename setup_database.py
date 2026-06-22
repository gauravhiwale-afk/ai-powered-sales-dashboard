import pandas as pd
import os
import sqlite3 

CSV_FILE = "superstore.csv"
DB_FILE = "sales.db"

print("Reading CSV...")
df = pd.read_csv(CSV_FILE, encoding="latin-1")

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

print("Creating database...")
conn = sqlite3.connect(DB_FILE)
df.to_sql("orders", conn, if_exists="replace", index=False)
conn.close()

print(" Database created successfully!")