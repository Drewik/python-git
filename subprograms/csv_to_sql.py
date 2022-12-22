import pandas as pd
import sqlite3

conn = sqlite3.connect("../sqlite_database.db")
df = pd.read_csv("../exchange_data.csv")
df.to_sql("exchange_data", conn, if_exists='replace', index=False)
conn.commit()
conn.close()
