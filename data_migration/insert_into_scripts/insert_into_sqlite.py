# insert records in all dataframe into a sqlite db named acero.db
import sqlite3

conn = sqlite3.connect("data_migration/data/acero_r.db")
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