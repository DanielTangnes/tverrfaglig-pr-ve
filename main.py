import os
from display import gui
import mysql.connector
import api
from tkinter import messagebox
import logging
import re

# Sett opp logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def connect_DB():
    server = 'mysql.ekvi.no'
    database = 'varehusdb'
    try:
        # Hent brukernavn og passord fra miljøvariabler
        username = os.environ['skoleMySQL']
        password = os.environ['pSkoleMySQL']
    except KeyError as e:
        # Vis feilmelding hvis miljøvariabler mangler
        messagebox.showerror('Environment Variable Error', f'Missing environment variable: {e}')
        logging.error(f'Missing environment variable: {e}')
        return None

    try:
        # Koble til databasen
        connection = mysql.connector.connect(
            host=server,
            database=database,
            user=username,
            password=password
        )
        logging.info('Database connection successful')
        return connection
    except mysql.connector.Error as err:
        # Vis feilmelding hvis tilkobling til databasen feiler
        messagebox.showerror('Database Connection Error', f'Error: {err}')
        logging.error(f'Database Connection Error: {err}')
        return None

def execute_procedure(procedure_name, params=()):
    # Koble til databasen
    connection = connect_DB()
    if connection:
        try:
            with connection.cursor() as cursor:
                # Utfør SQL-prosedyre eller spørring
                if procedure_name.lower().startswith("select"):
                    cursor.execute(procedure_name, params)
                    results = cursor.fetchall()
                else:
                    cursor.callproc(procedure_name, params)
                    results = []
                    for result in cursor.stored_results():
                        results.extend(result.fetchall())
                return results
        except mysql.connector.Error as err:
            # Vis feilmelding hvis spørring feiler
            messagebox.showerror('Database Query Error', f'Error: {err}')
            logging.error(f'Database Query Error: {err}')
        finally:
            # Lukk databasetilkoblingen
            connection.close()
    else:
        messagebox.showerror('Connection Error', 'Could not connect to the database.')
    return None

def ordre_db(tree2):
    # Hent ordreliste fra databasen og oppdater trestrukturen
    rows = execute_procedure('ordreliste')
    if rows:
        tree2.delete(*tree2.get_children())
        for row in rows:
            tree2.insert('', 'end', values=row)

def kunde_db(tree1):
    # Hent kundeliste fra databasen og oppdater trestrukturen
    rows = execute_procedure('alle_kunder')
    if rows:
        tree1.delete(*tree1.get_children())
        for row in rows:
            tree1.insert('', 'end', values=row)

def valgt_ordre_db(ordrenumer, tree):
    try:
        # Bruk regex for å hente ut det første tallet fra ordrenumer
        match = re.search(r'\d+', ordrenumer)
        if match:
            # Konverter det første tallet til et heltall
            ordrenumer = int(match.group())
            logging.info(f'Henter detaljer for ordrenummer: {ordrenumer}')
            # Utfør en prosedyre for å hente rader basert på ordrenummeret
            rows = execute_procedure('valgt_ordre', [ordrenumer])
            if rows:
                # Sett inn hver rad i trestrukturen
                for row in rows:
                    tree.insert('', 'end', values=row)
        else:
            # Kaster en feil hvis ingen gyldig ordrenummer ble funnet
            raise ValueError("Ingen gyldig ordrenummer funnet")
    except ValueError as e:
        # Viser en feilmelding hvis det oppstår en ValueError
        messagebox.showerror('Verdi Feil', f'Ugyldig ordrenummer: {e}')
        logging.error(f'Ugyldig ordrenummer: {e}')

def varehus_db(tree3):
    # Hent varehusdata fra databasen og oppdater trestrukturen
    rows = execute_procedure('varehus')
    if rows:
        tree3.delete(*tree3.get_children())
        for row in rows:
            tree3.insert('', 'end', values=row)

def opprette_kunde(fornavn, etternavn, adresse, postnr, tree1):
    # Opprett en ny kunde i databasen og oppdater kundelisten
    if execute_procedure("Ny_Kunde", (fornavn, etternavn, adresse, postnr)):
        kunde_db(tree1)

def slett_kunde(KNr, tree1):
    try:
        # Logg verdien som sendes til prosedyren
        logging.info(f'Prøver å slette kunde med KNr: {KNr}')
        if execute_procedure('SlettKunde', (KNr,)):
            kunde_db(tree1)
    except Exception as e:
        logging.error(f'Feil ved sletting av kunde: {e}')
        messagebox.showerror('Feil', f'Kunne ikke slette kunde: {e}')

def postkoder():
    # Hent postkoder fra databasen
    rows = execute_procedure("SELECT PostNr FROM poststed")
    if rows:
        return list(sum(rows, ()))
    return []

if __name__ == '__main__':
    logging.info('Starting GUI application')
    # Start GUI-applikasjonen og sett opp kommandoer
    root, tree1, tree2, tree3, fornavn_entry, etternavn_entry, adresse_entry, postnr_combo, selected_knr = gui(
        hent_ordreliste_cmd=lambda: ordre_db(tree2),
        hent_kundeliste_cmd=lambda: kunde_db(tree1),
        varehus_cmd=lambda: varehus_db(tree3),
        opprett_kunde_cmd=lambda: opprette_kunde(fornavn_entry.get(), etternavn_entry.get(), adresse_entry.get(), postnr_combo.get(), tree1),
        slett_kunde_cmd=lambda: slett_kunde(selected_knr.get(), tree1),
        hent_valgt_ordre_cmd=lambda ordrenr, tree: valgt_ordre_db(ordrenr, tree),
        postkoder_cmd=lambda: postkoder()
    )

    # Start API og GUI-hovedløkken
    api.run_api(connect_DB())
    root.mainloop()
    logging.info('GUI application ended')