from display import gui
import mysql.connector
import api


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
def ordre_db(tree2):
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
def kunde_db(tree1):
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
def valgt_ordre_db(ordrenumer, tree):
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
                    tree.insert('', 'end', values=row)

        finally:
            cursor.close()
            connection.close()


#Funksjon for henting av varelager
def varehus_db(tree3):
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
                    tree3.insert('', 'end', values=row)
        finally:
            cursor.close()
            connection.close()


#genererer kundenr for å opprette nye kunder
def generer_knr():
    connection = connect_DB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT MAX(KNr) FROM kunde")
            max_knr = cursor.fetchone()[0]
            if max_knr is None:
                new_knr = 1
            else:
                new_knr = max_knr + 1
            return new_knr
        finally:
            cursor.close()
            connection.close()


#Funksjon for opprettelse av kunde
def opprette_kunde(fornavn, etternavn, adresse, postnr):
    connection = connect_DB()
    knr = generer_knr()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                'INSERT INTO kunde (KNr, Fornavn, Etternavn, Adresse, PostNr) '
                'VALUES (%s, %s, %s, %s, %s);',
                (knr, fornavn, etternavn, adresse, postnr)
            )
            connection.commit()
        finally:
            cursor.close()
            connection.close()


def slett_kunde(KNr):
    connection = connect_DB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.callproc('SlettKunde', (KNr,))
            connection.commit()
        finally:
            cursor.close()
            connection.close()

#Henter posterkoder fra en oppdatert liste i databasen.
def postkoder():
    connection = connect_DB()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT PostNr FROM poststed")
            post_nr = cursor.fetchall()
            post_nr_liste = list(sum(post_nr, ()))

            return post_nr_liste
        finally:
            cursor.close()
            connection.close()

if __name__ == '__main__':
    root, tree1, tree2, tree3, fornavn_entry, etternavn_entry, adresse_entry, postnr_entry, selected_knr = gui(
        hent_ordreliste_cmd=lambda: ordre_db(tree2),
        hent_kundeliste_cmd=lambda: kunde_db(tree1),
        varehus_cmd=lambda: varehus_db(tree3),
        opprett_kunde_cmd=lambda: opprette_kunde(fornavn_entry.get(), etternavn_entry.get(), adresse_entry.get(), postnr_entry.get()),
        slett_kunde_cmd=lambda: slett_kunde(selected_knr.get()),
        hent_valgt_ordre_cmd=lambda ordrenr, tree: valgt_ordre_db(ordrenr, tree),
        postkoder_cmd=lambda: postkoder()
        )

    api.run_api(connect_DB())
    root.mainloop()