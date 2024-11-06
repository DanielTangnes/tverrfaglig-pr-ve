#import tkinter as tk
#from tkinter import ttk
import mysql.connector

def connect_DB():
    try:
        server = 'localhost' # Husk å endre til riktig servernavn (kan kjøre SHOW VARIABLES LIKE '%hostname%' for å finne navn)
        database = 'varehusdb'
        username = 'root'
        password = 'root'

        connection = mysql.connector.connect(
            host=server,
            database=database,
            user=username,
            password=password
        )

        return connection
    except Exception as e:
        return None

def hent_inventar():
    connection = connect_DB()
    if connection:
        cursor = connection.cursor()
        cursor.execute("select * from varehusdb.vare")
        orders = cursor.fetchall()
        connection.close()
        return orders
    return []

print(hent_inventar())
#test