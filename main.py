import tkinter as tk
from tkinter import ttk
import mysql.connector

def connect_DB():
    server = 'daniels-MacBook-Pro.local' # Husk å endre til riktig servernavn (kan kjøre SHOW VARIABLES LIKE '%hostname%' for å finne navn)
    database = 'varehusdb'
    username = 'root'
    password = ''

    connection = mysql.connector.connect(
        host=server,
        database=database,
        user=username,
        password=password
    )

    return connection

### Displayer tabell i GUI
root = tk.Tk()
root.title("test display")
root.geometry("600x400")
root.eval('tk::PlaceWindow . center')

tree = ttk.Treeview(root)
tree['columns'] = ("test1", "test2", "test3")

rows = connect_DB()
for row in rows:
    tree.insert("", "end", values=row)

tree.pack(pady=20)

root.mainloop()