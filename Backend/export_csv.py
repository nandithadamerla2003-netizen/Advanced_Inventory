import os
import pandas as pd
import mysql.connector
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME


connection = mysql.connector.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

os.makedirs("data", exist_ok=True)

tables = [
    "users",
    "suppliers",
    "products",
    "inventory",
    "purchases",
    "sales"
]

for table in tables:

    query = f"SELECT * FROM {table}"

    df = pd.read_sql(query, connection)

    filename = f"data/{table}.csv"

    df.to_csv(filename, index=False)

    print(f"{table}.csv created successfully")

connection.close()

print("\nAll CSV files created successfully!")