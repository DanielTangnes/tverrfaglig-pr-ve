import tkinter as tk
import mysql.connector

server = 'daniels-MacBook-Pro.local'
database = 'varehusdb'
username = 'root'
password = ''

# Establishing a connection to the MySQL database
cnxn = mysql.connector.connect(
    host=server,
    database=database,
    user=username,
    password=password
)

cursor = cnxn.cursor()

# Example query
cursor.execute("SHOW TABLES")
for table in cursor:
    print(table)

# Remember to close the cursor and connection when done
cursor.close()
cnxn.close()
