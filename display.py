import tkinter as tk
from tkinter import ttk, Toplevel
from ttkwidgets.autocomplete import AutocompleteCombobox
import logging

# Fargebibliotek
background_clr = '#fcf2e9'
tab_background_clr = '#fab97f'
button_clr = '#fab97f'
button_hover_clr = '#ff9600'
button_select_clr = '#ffb800'

def gui(hent_ordreliste_cmd=None, hent_kundeliste_cmd=None, opprett_kunde_cmd=None, varehus_cmd=None, slett_kunde_cmd=None, hent_valgt_ordre_cmd=None, postkoder_cmd=None):
    root = tk.Tk()
    root.title("Gruppe1 V1.1")
    root.geometry("1000x450")
    root.eval('tk::PlaceWindow . center')

    def on_tab_select(event):
        # Hent data når en fane velges
        selected_tab = tabControl.index(tabControl.select())
        if selected_tab == 0 and hent_kundeliste_cmd:
            hent_kundeliste_cmd()
        elif selected_tab == 1 and hent_ordreliste_cmd:
            hent_ordreliste_cmd()
        elif selected_tab == 2 and varehus_cmd:
            varehus_cmd()

    selected_knr = tk.StringVar()

    def on_treeview_click(event):
        # Hent valgt kunde når en rad i treet klikkes
        selected_item = tree1.selection()
        if selected_item:
            item_values = tree1.item(selected_item)["values"]
            if item_values:
                selected_knr.set(item_values)  # Sett kun kundenummeret
                logging.info(f"Kundenr {selected_knr.get()} valgt")

    selected_ordre = tk.StringVar()

    def open_popup(event, fetch_ordre_detaljer):
        # Åpne popup-vindu for å vise ordredetaljer
        selected_item = tree2.selection()
        if selected_item:
            item_values = tree2.item(selected_item)["values"]
            if item_values:
                selected_ordre.set(item_values)
                print(f"Ordre {selected_ordre.get()} valgt")

                top = Toplevel(root)
                top.geometry("")
                top.title(f"Ordre Detaljer for ordre {selected_ordre.get()}")

                tree_popup = ttk.Treeview(top, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8"), show='headings')
                for i, col in enumerate(["KNr", "Fornavn", "Etternavn", "Adresse", "Ordre Nummer", "Antall", "Sum", "Betegnelse"], 1):
                    tree_popup.column(f"#{i}", anchor=tk.CENTER, width=150)
                    tree_popup.heading(f"#{i}", text=col)
                tree_popup.pack(fill=tk.BOTH, expand=True)

                fetch_ordre_detaljer(selected_ordre.get(), tree_popup)

    tabControl = ttk.Notebook(root)

    style = ttk.Style()
    style.theme_use('default')
    style.configure('TNotebook', background=tab_background_clr)
    style.configure('TNotebook.Tab', background=button_clr)
    style.map('TNotebook.Tab', background=[('selected', button_hover_clr), ('active', button_select_clr)])
    style.configure('TButton', background=button_clr)
    style.map('TButton', background=[('active', button_hover_clr), ('active', button_select_clr)])

    tab1 = tk.Frame(tabControl, background=background_clr)
    tab2 = tk.Frame(tabControl, background=background_clr)
    tab3 = tk.Frame(tabControl, background=background_clr)

    tabControl.bind("<<NotebookTabChanged>>", on_tab_select)

    tabControl.add(tab1, text="Kunde")
    tabControl.add(tab2, text="Ordre")
    tabControl.add(tab3, text="Varehus")
    tabControl.pack(expand=1, fill="both")

    tree1 = ttk.Treeview(tab1, column=("c1", "c2", "c3", "c4", "c5"), show='headings')
    for i, col in enumerate(["Kundenr", "Fornavn", "Etternavn", "Adresse", "Postnr"], 1):
        tree1.column(f"#{i}", anchor=tk.CENTER)
        tree1.heading(f"#{i}", text=col)
    tree1.bind("<ButtonRelease-1>", on_treeview_click)
    tree1.pack()

    tree2 = ttk.Treeview(tab2, column=("c1", "c2", "c3", "c4", "c5"), show='headings')
    for i, col in enumerate(["OrdreNr", "OrdreDato", "SendtDato", "BetaltDato", "KundeNr"], 1):
        tree2.column(f"#{i}", anchor=tk.CENTER)
        tree2.heading(f"#{i}", text=col)
    tree2.bind("<Double-1>", lambda event: open_popup(event, hent_valgt_ordre_cmd))
    tree2.pack()

    tree3 = ttk.Treeview(tab3, column=("c1", "c2", "c3", "c4", "c5", "c6"), show='headings')
    for i, col in enumerate(["VareNr", "Betegnelse", "Pris", "Katogori nr", "Antall", "Hylle"], 1):
        tree3.column(f"#{i}", anchor=tk.CENTER)
        tree3.heading(f"#{i}", text=col)
    tree3.pack()

    entry_frame = tk.Frame(tab1)
    entry_frame.pack(pady=10)

    #Inndatafelter for opprett kunde funkesjoner.
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

    post_nr = postkoder_cmd()
    postnr_combo = AutocompleteCombobox(entry_frame, completevalues=post_nr, state="readonly")
    postnr_combo.grid(row=0, column=3, padx=5)
    postnr_combo.bind("<Button-1>", lambda e: postnr_combo.delete(0, tk.END))
    postnr_combo.insert(0, "Postnr")

    button1 = ttk.Button(tab2, text="Oppdater Ordreliste", command=hent_ordreliste_cmd)
    button1.pack(pady=10)

    button2 = ttk.Button(tab1, text="Oppdater Kundeliste", command=hent_kundeliste_cmd)
    button2.pack(pady=10)
    button3 = ttk.Button(tab1, text="Opprett Kunde", command=opprett_kunde_cmd)
    button3.pack(pady=10)
    button4 = ttk.Button(tab1, text="Slett Kunde", command=slett_kunde_cmd)
    button4.pack(pady=10)

    button5 = ttk.Button(tab3, text="Oppdater Varehus", command=varehus_cmd)
    button5.pack(pady=10)

    return root, tree1, tree2, tree3, fornavn_entry, etternavn_entry, adresse_entry, postnr_combo, selected_knr