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
    print(tables)
    for table in tables:
        print(table[0])

except Error as e:
    print(e)
finally:
    for file in csv_files:
        file_path = os.path.join(datadirs, file)

        try:
            # Read CSV into a DataFrame and append to the list
            df.append(pd.read_csv(file_path))
            print("File opened successfully")
        except Error as e:
            print(e)

combined = pd.merge(df[1],df[2],on = "shipment_identifier")
sel = combined[['product']] already inserted the product data to database so i commented this snippet
name  = sel.drop_duplicates()
name.rename(columns={'product': 'name'}, inplace=True)
name.to_sql('product', conn, index=False, if_exists='append')
print(name)

colums = ['driver_identifier','on_time']
combined.drop(colums, inplace=True, axis=1)
c1 = pd.merge(df[0],combined,on = "product")
c1.drop(['origin_warehouse_y','destination_store_y','driver_identifier','on_time'], inplace=True, axis=1)
c1.rename(columns={'origin_warehouse_x': 'origin','destination_store_x':'destination','product_quantity':'quantity','product':'name'}, inplace=True)
try:
    sql_query = "SELECT * FROM product"
except Error as e:
    print(e)
finally:
    products = pd.read_sql(sql_query, conn)
    c3 = pd.merge(c1,products,on = "name")
    c3.drop(['name','shipment_identifier'], inplace=True, axis=1)
    c3.rename(columns={'id': 'product_id'}, inplace=True)
    print(c3.columns)
    c3.to_sql('shipment', conn, index=False, if_exists='append')
    conn.close()
