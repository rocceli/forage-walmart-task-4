import csv
import os
import sqlite3
import pandas as pd
from sqlite3 import Error

print('am in')
db_file = 'shipment_database.db'
table1 = 'shipment'
table2 = 'products'

datadirs = 'data'

csv_files = [f for f in os.listdir(datadirs) if f.endswith('.csv')]
print(csv_files)

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
        df1 = pd.read_csv(file_path)
        print(df1.columns)
        try:
             open(file_path, 'r')
        except Error as e:
                print(e)
        finally:
                print("File opened successfully")
                with open(file_path, 'r') as f:
                    reader = csv.reader(open(file_path, 'r'),delimiter=',')
                    for read in reader:
                        i = 0
                        # print(read)
                        # for item in read:
                        #     print(item)
                        #     break
                            # column_data = row[i]
                            # # cursor.execute('INSERT INTO ' + table1 +(row) + VALUES ()+column_data)'
                            # i+=1
                            # print(column_data)