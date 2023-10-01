import csv
import os
import sqlite3
import pandas as pd
from sqlite3 import Error

db_file = 'shipment_database.db'
table1 = 'shipment'
table2 = 'products'

datadirs = 'data'

csv_files = [f for f in os.listdir(datadirs) if f.endswith('.csv')]
print(csv_files)
df = []  # Initialize an empty list to store DataFrames

try:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in the database:")
    for table in tables:
        print(table[0])
except Error as e:
    print(e)
finally:
    for file in csv_files:
        file_path = os.path.join(datadirs, file)
        
        try:
            df.append(pd.read_csv(file_path))  # Read CSV into a DataFrame and append to the list
            print("File opened successfully")
        except Error as e:
            print(e)

combined = pd.merge(df[1],df[2],on = "shipment_identifier")
sel = combined[['product']]
name  = sel.drop_duplicates()
name.rename(columns={'product': 'name'})
name.to_sql('shipment', conn, index=False, if_exists='append')  
print(name)
    
