import tkinter as tk
from tkinter import ttk
import mysql.connector

def connect_DB():
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

    cursor.execute("select * from ansatt")
    rows = cursor.fetchall()
    cnxn.close()

    return rows

### Displayer tabell i GUI
root = tk.Tk()
root.title("test display")
root.geometry("600x400")

tree = ttk.Treeview(root)
tree['columns'] = ("test1", "test2", "test3")

rows = connect_DB()
for row in rows:
    tree.insert("", "end", values=row)

tree.pack(pady=20)

root.mainloop()