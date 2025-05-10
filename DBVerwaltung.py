"""
Created on 18.12.2019
@author: Anselm Heuer
Version 1.2 - last change on 14.04.2025
Hier wird eine Klasse zur Kommunikation mit einer SQL-Datenbank bereitgestellt. Zum Beispiel für das Kaffeekassentool
--A class for communication with an SQL database is provided here. For example, for the coffee tool--
--Comments in functions are partly written in German - can easily be translated into english with translation programs :)--
"""
# Import all relevant functions
import sqlite3


class DBVerwaltung_SQL:
    """
    Mit dieser Klasse kann auf eine SQL-Datenbank zugegriffen werden. Es werden Methoden bereit gestellt um z. B. neue Zeilen in eine Tabelle
    zu schreiben. Offensichtliche Fehler beim Datenbankzugriff werden in den entsprechenden Methoden abgefangen. Dem Nutzer wird somit der
    Zugriff auf die Datenbank erleichtert.

    Methoden:
    - [LeseAlleZeilen] Gibt alle Zeilen aus der angegebenen Tabelle zurueck
    - [LeseSpezielleZeilen] Gibt nur die Zeilen in der angegebenen Tabelle zurueck, die die uebergebene Bedingung erfuellen
    - [SchreibeNeueZeilen] Es wird eine oder mehrere neue Zeile(n) in die angegebene Tabelle geschrieben
    - [UeberschreibeZeile] Es wird an einer bestehenden Zeile ein oder mehrere Wert(e) veraendert, fuer die die uebergebene Bedingung erfuellt ist
    - [LoescheSpezielleZeile] Es wird eine bestehende Zeile geloescht, fuer die die uebergebene Bedingung erfuellt ist
    """

    def __init__(self, NameDatenbank):
        self.__connection = sqlite3.connect(NameDatenbank)
        self.__cursor = self.__connection.cursor()

    def __del__(self):
        # Datenbank wieder frei geben
        self.__connection.close()

    def __LeseVariablenTabelle(self, NameTabelle):
        # Es werden fuer eine gegebene Tabelle die Spaltennamen (Variablen) zurueck gegeben, die dort enthalten sind
        self.__cursor.execute("PRAGMA table_info({})".format(NameTabelle))
        Daten = self.__cursor.fetchall()
        Spaltennamen = []
        for Spaltenname in Daten:
            Spaltennamen.append(Spaltenname[1])
        return Spaltennamen

    def LeseAlleZeilen(self, NameTabelle):
        # Der gesamte Inhalt (alle Zeilen) der Tabelle wird zurueck gegeben.
        self.__cursor.execute("SELECT * FROM {}".format(NameTabelle))
        return self.__cursor.fetchall()

    def LeseSpezielleZeilen(self, NameTabelle, Bedingung):
        # Nur Zeilen, die die Bedingung erfuellen, werden zurueckgegeben. Die Bedingung muss als String uebergeben werden.
        # Bedingungen haben die Form: 'Variablenname=Wert' Also z. B.: 'produkt="Kaffeebohnen"'
        self.__cursor.execute("SELECT * FROM {} WHERE {};".format(NameTabelle, Bedingung))
        return self.__cursor.fetchall()

    def SchreibeNeueZeilen(self, NameTabelle, SQLTeilBefehl, **VariablenDaten):
        # Mit dieser Methode koennen neue Zeilen in die bestehende Tabelle geschrieben werden.
        # SQLTeilBefehl hat die Form: "Variblenname1, Variablenname2, ..." und muss als String uebergeben werden. Also z. B.: "produkt, anzahl, aktiv, soll, kosten"
        # VariablenDaten enthaehlt zu den Variblennamen (siehe SQLTeilBefehl) die passenden Werte und wird NICHT als String uebergeben.
        # Es hat also die Form: Variablenname=Wert Also z. B. für den SQLTeilBefehl von oben: produkt="Gans", anzahl=5, aktiv=0, soll=10, kosten=10
        VariablenInTabelle = self.__LeseVariablenTabelle(NameTabelle)
        if len(VariablenDaten) == len(VariablenInTabelle)-1:
            SQLBefehl = "INSERT INTO {}({}) VALUES(".format(NameTabelle, SQLTeilBefehl)
            counter = 1
            for key, value in VariablenDaten.items():
                if key == VariablenInTabelle[counter]:
                    if isinstance(value, str):
                        if "datetime" in value:  # So kann der Befehl in SQLite ohne Anfuehrungszeichen (") ausgefuehrt werden
                            SQLBefehl += value + ", "
                        else:
                            SQLBefehl += '"' + str(value) + '", '
                    else:
                        SQLBefehl += str(value) + ", "
                    counter += 1
                else:
                    print("Fehler: Uebergebene VariablenDaten passen nicht zu Variablen in der Tabelle")
                    break
            SQLBefehl = SQLBefehl[:-2] + ");"
            self.__cursor.execute(SQLBefehl)
            self.__connection.commit()  # Nicht vergessen, wenn die Aenderungen gespeichert werden sollen!
        else:
            print("Fehler: Uebergebene VariablenDaten passen nicht zu Anzahl der Variablen in der Tabelle!")

    def UeberschreibeZeile(self, NameTabelle, Bedingung, **VariablenDaten):
        # Es können in einer bestehenden Tabelle und bestehenden Zeile Werte veraendert werden. Dazu muss eine Bedingung uebergeben werden.
        # Die Bedingung muss als String uebergeben werden. Bedingungen haben die Form Variablenname=Wert. Also z. B.: 'produkt="Kaffeebohnen"'
        # VariablenDaten enthaehlt zu den Variablennamen die passenden Werte und wird NICHT als Sring uebergeben.
        # Es hat also die Form: Variablenname=Wert Also z. B.: soll=3
        SQLTeilBefehl = ""
        for key, value in VariablenDaten.items():
            if isinstance(value, str):
                if "datetime" in value:  # So kann der Befehl in SQLite ohne Anfuehrungszeichen (") ausgefuehrt werden
                    SQLTeilBefehl += str(key) + '=' + str(value) + ', '
                else:
                    SQLTeilBefehl += str(key) + '="' + str(value) + '", '
            else:
                SQLTeilBefehl += str(key) + "=" + str(value) + ", "
        SQLTeilBefehl = SQLTeilBefehl[:-2]
        self.__cursor.execute("UPDATE {} SET {} WHERE {};".format(NameTabelle, SQLTeilBefehl, Bedingung))
        self.__connection.commit()  # Nicht vergessen, wenn die Aenderungen gespeichert werden sollen!

    def LoescheSpezielleZeile(self, NameTabelle, Bedingung):
        # Es kann in einer Tabelle eine Zeile geloescht werden. Dazu muss eine Bedingung uebergeben werden. Die Bedingung muss zu einer
        # einzigartigen Zeile fuehren --> das wird ueberprueft! Es werden somit nicht mehrere Zeilen gleichzeitig geloescht.
        # Die Bedingung muss als String uebergeben werden. Bedingungen haben die Form Variablenname=Wert. Also z. B.: 'Nutzer="Albert Einstein"'
        if len(self.LeseSpezielleZeilen(NameTabelle, Bedingung)) == 1:
            self.__cursor.execute("DELETE FROM {} WHERE {};".format(NameTabelle, Bedingung))
            self.__connection.commit()  # Nicht vergessen, wenn die Aenderungen gespeichert werden sollen!
        else:
            print("Fehler: Die Bedingung adressiert nicht eine einzigartige Zeile")


if __name__ == '__main__':
    """
    # Tests der Klasse DBVerwaltung_SQL werden auf der Datenbank vom Kaffeekassentool ausgefuehrt
    TestDB = DBVerwaltung_SQL("KKT_database.sqlite")  # Es gibt zum Beispiel die Tabellen: Bestand, Bestellung, Nutzer (Stand 2022)
    print(TestDB.LeseAlleZeilen("Bestand"))
    TestDB.SchreibeNeueZeilen("Bestand", "produkt, anzahl, aktiv, soll, kosten", produkt="Gans", anzahl=5, aktiv=0, soll=10, kosten=10)
    print(TestDB.LeseAlleZeilen("Bestand"))
    print("---------------------------------")
    TestDB.UeberschreibeZeile("Bestand", 'produkt="Gans"', soll=3)
    print(TestDB.LeseAlleZeilen("Nutzer"))
    TestDB.UeberschreibeZeile("Nutzer", 'name="Albert Einstein"', kontostand=0)
    print(TestDB.LeseAlleZeilen("Bestand"))
    print(TestDB.LeseAlleZeilen("Nutzer"))
    print("---------------------------------")
    TestDB.LeseSpezielleZeilen("Bestand", 'produkt="Kaffeebohnen"')
    TestDB.LoescheSpezielleZeile("Nutzer", 'rang=0')
    TestDB.LoescheSpezielleZeile("Nutzer", 'name="Albert Einstein"')
    print(TestDB.LeseAlleZeilen("Nutzer"))
    """
