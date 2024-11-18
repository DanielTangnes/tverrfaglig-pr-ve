import tkinter as tk
from tkinter import ttk


def gui(hent_ordreliste_cmd=None, hent_kundeliste_cmd=None, opprett_kunde_cmd=None):
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

    button1 = tk.Button(tab2, text="Hent Ordreliste", command=hent_ordreliste_cmd)
    button1.pack(pady=10)
    button2 = tk.Button(tab1, text="Hent Kundeliste", command=hent_kundeliste_cmd)
    button2.pack(pady=10)
    button3 = tk.Button(tab1, text="Opprett Kunde", command=opprett_kunde_cmd)
    button3.pack(pady=10)

    return root, tree1, tree2, fornavn_entry, etternavn_entry, adresse_entry, postnr_entry