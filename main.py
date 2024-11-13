import tkinter as tk
from tkinter import ttk
import mysql.connector
from flask import Flask, jsonify
import threading

app = Flask(__name__)
def run_flask():
    app.run()

flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

def connect_DB():
    server = 'localhost'  # Husk å endre til riktig servernavn (kan kjøre SHOW VARIABLES LIKE '%hostname%' for å finne navn)
    database = 'varehusdb'
    username = 'root'
    password = 'root'
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

def ordre_db():
    connection = connect_DB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.callproc('alle_ordre')

            # Fetch the results from the stored procedure
            for result in cursor.stored_results():
                rows = result.fetchall()
                for row in rows:
                    print(row)
                    tree2.insert('', 'end', values=row)
        finally:
            cursor.close()
            connection.close()


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
            

@app.route('/api/test', methods=['GET'])
def api_test():
    con = connect_DB()
    cur = con.cursor()
    cur.execute('SELECT * FROM vare')
    rows = cur.fetchall()
    con.close()
    return jsonify(rows)

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


tree1 = ttk.Treeview(tab1, column=("c1", "c2", "c3"), show='headings')
tree1.column("#1", anchor=tk.CENTER)
tree1.heading("#1", text="ID")
tree1.column("#2", anchor=tk.CENTER)
tree1.heading("#2", text="FNAME")
tree1.column("#3", anchor=tk.CENTER)
tree1.heading("#3", text="LNAME")
tree1.pack()
button1 = tk.Button(tab2, text="Hent Ordre", command= ordre_db)
button1.pack(pady=10)
button2 = tk.Button(tab1, text="Hent Kunde", command= kunde_db)
button2.pack(pady=10)



root.mainloop()