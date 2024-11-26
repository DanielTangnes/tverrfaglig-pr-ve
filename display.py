import tkinter as tk
from tkinter import ttk, Button, Toplevel

#Fargebibliotek
background_clr = '#fcf2e9'
tab_background_clr = '#fab97f'
button_clr = '#fab97f'
button_hover_clr = '#ff9600'
button_select_clr = '#ffb800'

def gui(hent_ordreliste_cmd=None, hent_kundeliste_cmd=None, opprett_kunde_cmd=None, varehus_cmd=None, slett_kunde_cmd=None, hent_valgt_ordre_cmd=None):
    root = tk.Tk()
    root.title("Gruppe1 V0.3")
    root.geometry("1000x450")
    root.eval('tk::PlaceWindow . center')

    #funksjon for automatisk utfylling av tabeler når tab åpnes.
    def on_tab_select(event):
        selected_tab = tabControl.index(tabControl.select())
        if selected_tab == 0:
            if hent_kundeliste_cmd:
                hent_kundeliste_cmd()
            print("Kunde tab selected")
            # Placeholder command for Kunde tab
        elif selected_tab == 1:
            if hent_ordreliste_cmd:
                hent_ordreliste_cmd()
            print("Ordre tab selected")
            # Placeholder command for Ordre tab
        elif selected_tab == 2:
            if varehus_cmd:
                varehus_cmd()
            print("Varehus tab selected")


    selected_knr = tk.StringVar()


    def on_treeview_click(event):
        selected_item = tree1.selection()  # Hent valgt data
        if selected_item:
            item_values = tree1.item(selected_item)["values"]
            if item_values:
                selected_knr.set(item_values[0])  # Lagre Kundenr til StringVar
                print("Kundenr {} valgt".format(selected_knr.get()))


    selected_ordre = tk.StringVar()

    def open_popup(event, fetch_ordre_detaljer):
        selected_item = tree2.selection()
        if selected_item:
            item_values = tree2.item(selected_item)["values"]
            if item_values:
                selected_ordre.set(item_values[0])  # Lagre OrdreNr
                print("Ordre {} valgt".format(selected_ordre.get()))

                top = Toplevel(root)
                top.geometry("500x250")
                top.title("Ordre Detaljer for ordre {}".format(selected_ordre.get()))

                tree_popup = ttk.Treeview(top, columns=("col1", "col2", "col3", "col4"), show='headings')
                tree_popup.column("#1", anchor=tk.CENTER, width=100)
                tree_popup.heading("#1", text="OrdreNr")
                tree_popup.column("#2", anchor=tk.CENTER, width=150)
                tree_popup.heading("#2", text="VNr")
                tree_popup.column("#3", anchor=tk.CENTER, width=150)
                tree_popup.heading("#3", text="PrisPrEnhet")
                tree_popup.column("#4", anchor=tk.CENTER, width=150)
                tree_popup.heading("#4", text="Antall")
                tree_popup.pack(fill=tk.BOTH, expand=True)

                fetch_ordre_detaljer(selected_ordre.get(), tree_popup)


    tabControl = ttk.Notebook(root)

    #Stilcbibliotek
    style = ttk.Style()
    style.theme_use('default')
    #Stil for bakgrunn på tab bar
    style.configure('TNotebook', background=tab_background_clr)
    #stil for farger på tabs basert på om de er aktive, inaktive eller musepekeren er over fanen.
    style.configure('TNotebook.Tab', background=button_clr)
    style.map('TNotebook.Tab', background=[('selected', button_hover_clr), ('active', button_select_clr)])

    #Stil for alle knapper i applikasjonen
    style.configure('TButton', background=button_clr)
    style.map('TButton', background=[('active', button_hover_clr), ('active', button_select_clr)])

    #setter farger på alle tabs
    tab1 = tk.Frame(tabControl, background=background_clr)
    tab2 = tk.Frame(tabControl, background=background_clr)
    tab3 = tk.Frame(tabControl, background=background_clr)


    tabControl.bind("<<NotebookTabChanged>>", on_tab_select)


    tabControl.add(tab1, text="Kunde",)
    tabControl.add(tab2, text="Ordre")
    tabControl.add(tab3, text="Varehus")

    tabControl.pack(expand=1, fill="both")

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
    tree1.bind("<ButtonRelease-1>", on_treeview_click)
    tree1.pack()

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
    tree2.bind("<Double-1>", lambda event: open_popup(event, hent_valgt_ordre_cmd))
    tree2.pack()

    tree3 = ttk.Treeview(tab3, column=("c1", "c2", "c3", "c4", "c5", "c6"), show='headings')
    tree3.column("#1", anchor=tk.CENTER)
    tree3.heading("#1", text="VareNr")
    tree3.column("#2", anchor=tk.CENTER)
    tree3.heading("#2", text="Betegnelse")
    tree3.column("#3", anchor=tk.CENTER)
    tree3.heading("#3", text="Pris")
    tree3.column("#4", anchor=tk.CENTER)
    tree3.heading("#4", text="Katogori nr")
    tree3.column("#5", anchor=tk.CENTER)
    tree3.heading("#5", text="Antall")
    tree3.column("#6", anchor=tk.CENTER)
    tree3.heading("#6", text="Hylle")
    tree3.pack()

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

    #knapper i ordretab
    button1 = ttk.Button(tab2, text="Oppdater Ordreliste", command=hent_ordreliste_cmd)
    button1.pack(pady=10)

    # knapper i kundetab
    button2 = ttk.Button(tab1, text="Oppdater Kundeliste", command=hent_kundeliste_cmd)
    button2.pack(pady=10)
    button3 = ttk.Button(tab1, text="Opprett Kunde", command=opprett_kunde_cmd)
    button3.pack(pady=10)
    button4 = ttk.Button(tab1, text="Slett Kunde", command=slett_kunde_cmd)
    button4.pack(pady=10)

    #Knapper i Varehus tab
    button5 = ttk.Button(tab3, text="Oppdater Varehus", command=varehus_cmd, style='TButton')
    button5.pack(pady=10)

    return root, tree1, tree2, tree3, fornavn_entry, etternavn_entry, adresse_entry, postnr_entry, selected_knr