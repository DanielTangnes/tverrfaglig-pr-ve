import tkinter as tk
from tkinter import ttk
import mysql.connector

def connect_DB():
    server = 'localhost' # Husk å endre til riktig servernavn (kan kjøre SHOW VARIABLES LIKE '%hostname%' for å finne navn)
    database = 'varehusdb'
    username = 'root'
    password = 'passord123'

    connection = mysql.connector.connect(
        host=server,
        database=database,
        user=username,
        password=password
    )

    return connection

def ordre():
    con1 = connect_DB()
    cur1 = con1.cursor()
    cur1.execute('SELECT * FROM ordre')
    rows = cur1.fetchall()
    for row in rows:
        print(row)
        tree2.insert('', 'end', values=row)
    con1.close()

def kunde():
    con2 = connect_DB()
    cur2 = con2.cursor()
    cur2.execute('SELECT * FROM kunde')
    rows = cur2.fetchall()
    for row in rows:
        print(row)
        tree1.insert('', 'end', values=row)
    con2.close()

### Displayer tabell i GUI
root = tk.Tk()
root.title("test display")
root.geometry("600x400")
root.eval('tk::PlaceWindow . center')
tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text="Kunde")
tabControl.add(tab2, text="Ordre")

tabControl.pack(expand=1, fill="both")


tree1 = ttk.Treeview(tab1, column=("c1", "c2", "c3"), show='headings')
tree1.column("#1", anchor=tk.CENTER)
tree1.heading("#1", text="ID")
tree1.column("#2", anchor=tk.CENTER)
tree1.heading("#2", text="FNAME")
tree1.column("#3", anchor=tk.CENTER)
tree1.heading("#3", text="LNAME")
tree1.pack()
button1 = tk.Button(tab1, text="Oppdater ordre", command= kunde)
button1.pack(pady=10)

tree2 = ttk.Treeview(tab2, column=("c1", "c2", "c3", "c4", "c5"), show='headings')
tree2.column("#1", anchor=tk.CENTER)
tree2.heading("#1", text="OrdreNr")
tree2.column("#2", anchor=tk.CENTER)
tree2.heading("#2", text="OrdreDato")
tree2.column("#3", anchor=tk.CENTER)
tree2.heading("#3", text="SendtDato")
tree2.column("#4", anchor=tk.CENTER)
tree2.heading("#4", text="BetaltDato")
tree2.column("#5", anchor=tk.CENTER)
tree2.heading("#5", text="KundeNr")
tree2.pack()
button2 = tk.Button(tab2, text="Oppdater kunde", command= ordre)
button2.pack(pady=10)

root.mainloop()