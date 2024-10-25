import tkinter as tk
import pyodbc

server = 'your_server_name'
database = 'your_database_name'
username = 'your_username'
password = 'your_password'

# Establishing a connection to the SQL Server
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};\
                      SERVER='+server+';\
                      DATABASE='+database+';\
                      UID='+username+';\
                      PWD='+ password)

cursor = cnxn.cursor()

def connect_db():


def display_varelager():