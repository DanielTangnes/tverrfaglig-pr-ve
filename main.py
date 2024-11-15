import tkinter as tk
from tkinter import ttk
import mysql.connector
from flask import Flask, jsonify
import threading
import pandas as pd

app = Flask(__name__)
def run_flask():
    app.run()

flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

def connect_DB():
    server = 'mysql.ekvi.no'  # Husk å endre til riktig servernavn (kan kjøre SHOW VARIABLES LIKE '%hostname%' for å finne navn)
    database = 'varehusdb'
    username = '23ITDNett'
    password = 'TVERRFAGLIG'
    try:
        connection = mysql.connector.connect(
            host=server,
            database=database,
            user=username,
            password=password
        )
        return connection
    except Exception as e:
        return None

#Funksjon for henting av ordreliste
def ordre_db():
    connection = connect_DB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.callproc('ordreliste')

            # Fetch the results from the stored procedure
            for result in cursor.stored_results():
                rows = result.fetchall()
                for row in rows:
                    print(row)
                    tree2.insert('', 'end', values=row)
        finally:
            cursor.close()
            connection.close()

#Funksjon for henting av kundeliste
def kunde_db():
    connection = connect_DB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.callproc('alle_kunder')

            # Fetch the results from the stored procedure
            for result in cursor.stored_results():
                rows = result.fetchall()
                for row in rows:
                    print(row)
                    tree1.insert('', 'end', values=row)
        finally:
            cursor.close()
            connection.close()

#Funksjon for henting av detaljer rundt en valgt ordre
def valgt_ordre_db(ordrenumer):
    connection = connect_DB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.callproc('valgt_ordre', [ordrenumer,])

            # Fetch the results from the stored procedure
            for result in cursor.stored_results():
                rows = result.fetchall()
                for row in rows:
                    print(row)
                    tree1.insert('', 'end', values=row)
        finally:
            cursor.close()
            connection.close()

#Funksjon for henting av varelager
def varehus_db():
    connection = connect_DB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.callproc('varehus')

            # Fetch the results from the stored procedure
            for result in cursor.stored_results():
                rows = result.fetchall()
                for row in rows:
                    print(row)
                    tree1.insert('', 'end', values=row)
        finally:
            cursor.close()
            connection.close()

#Funksjon for opprettelse av kunde
def opprette_kunde():
    connection = connect_DB()
    if connection:
        try:
            cursor = connection.cursor()



        finally:
            cursor.close()
            connection.close()


@app.route('/api/test', methods=['GET'])
def api_test():
    con = connect_DB()
    cur = con.cursor()
    cur.execute('SELECT * FROM vare')
    names = [x[0] for x in cur.description]
    rows = cur.fetchall()
    con.close()
    df = pd.DataFrame(rows, columns=names)
    return jsonify(df.to_dict(orient='records'))

### Displayer tabell i GUI
root = tk.Tk()
root.title("test display")
root.geometry("1000x400")
root.eval('tk::PlaceWindow . center')
tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text="Kunde")
tabControl.add(tab2, text="Ordre")

tabControl.pack(expand=1, fill="both")

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


tree1 = ttk.Treeview(tab1, column=("c1", "c2", "c3", "c4", "c5"), show='headings')
tree1.column("#1", anchor=tk.CENTER)
tree1.heading("#1", text="Kundenr")
tree1.column("#2", anchor=tk.CENTER)
tree1.heading("#2", text="Fornavn")
tree1.column("#3", anchor=tk.CENTER)
tree1.heading("#3", text="Etternavn")
tree1.column("#4", anchor=tk.CENTER)
tree1.heading("#4", text="Adressse")
tree1.column("#5", anchor=tk.CENTER)
tree1.heading("#5", text="Postnr")
tree1.pack()

entry_frame = tk.Frame(tab1)
entry_frame.pack(pady=10)

fornavn_entry = tk.Entry(entry_frame)
fornavn_entry.grid(row=0, column=0, padx=5)
fornavn_entry.bind("<Button-1>", lambda e: fornavn_entry.delete(0, tk.END))
fornavn_entry.insert(0, "Fornavn")

etternavn_entry = tk.Entry(entry_frame)
etternavn_entry.grid(row=0, column=1, padx=5)
etternavn_entry.bind("<Button-1>", lambda e: etternavn_entry.delete(0, tk.END))
etternavn_entry.insert(0, "Etternavn")

adresse_entry = tk.Entry(entry_frame)
adresse_entry.grid(row=0, column=2, padx=5)
adresse_entry.bind("<Button-1>", lambda e: adresse_entry.delete(0, tk.END))
adresse_entry.insert(0, "Adresse")

postnr_entry = tk.Entry(entry_frame)
postnr_entry.grid(row=0, column=3, padx=5)
postnr_entry.bind("<Button-1>", lambda e: postnr_entry.delete(0, tk.END))
postnr_entry.insert(0, "Postnr")

def opprett_kunde_pressed():
    fornavn = fornavn_entry.get()
    etternavn = etternavn_entry.get()
    adresse = adresse_entry.get()
    postnr = postnr_entry.get()
    opprette_kunde(fornavn, etternavn, adresse, postnr)

button1 = tk.Button(tab2, text="Hent Ordreliste", command= ordre_db)
button1.pack(pady=10)
button2 = tk.Button(tab1, text="Hent Kundeliste", command= kunde_db)
button2.pack(pady=10)
button3 = tk.Button(tab1, text="Opprett Kunde", command= opprett_kunde_pressed)
button3.pack(pady=10)



root.mainloop()