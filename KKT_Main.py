"""
Created on 05.12.2019
@author: Anselm Heuer
Version 1.8 - last change on 27.04.2025
Software fuer die digitale Kaffeekueche - Das Tool zum Abrechnen von Produkten bei vielen Nutzern!
--Software for the digital coffee kitchen - The tool for billing products for many users!--
--Comments in functions are partly written in German - can easily be translated into english with translation programs :)--
"""
# Import all relevant functions and outsourced modules
import DBVerwaltung, GUIElemente, KKT_Verwaltung, KKT_Parameter
from datetime import datetime, timedelta
# modules for Gtk
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib
# modules for graph creation
from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib.figure import Figure
import numpy as np

import random
Zufallszahl = random.Random()
Zufallszahl.seed()


class MainWindow:
    """
    Eine Software fuer die digitale Kaffeekueche. Es wird eine grafische Benutzeroberflaeche (GUI) aufgebaut und um viele weitere nuetzliche Funktionen erweitert,
    sodass Nutzer der Kaffeekueche bequem Produkte (ohne laestige analoge Listen) abrechnen koennen!
    Technisch gesehen werden aus einer Glade-Datei die vorgefertigten GUI-Elemente gelesen und diese dann erweitert und angepasst. Es werden viele Funktionen
    bereitgestellt um z. B. den Buttons in der GUI eine Funktion zu geben. Teilweise stehen in der Glade-Datei bzw. in den vorgefertigten GUI-Elementen schon
    die Namen der Funktionen drin, die dann an dieser Stelle bereitgestellt werden muessen. Es findet in diesem Fall eine Verkuepfung statt, weshalb manche
    Funktionsnamen nicht mehr veraendert werden duerfen (in der Regel Funktionen mit "on_XXX_YYY" im Namen). Die Glade-Datei kann z. B. mit einer Software wie
    "Glade" bearbeitet werden. Die meisten Funktionen in dieser Klasse sind nicht fuer den externen Zugang gedacht und sollten bzw. koennen nicht extern
    aufgerufen werden. Ein paar wenige Funktionen duerfen von extern aufgerufen werden und sind im Folgenden beschrieben ...

    Methoden:
    - [StartenGUIKKT] Hiermit wird die Software fuer die digitale Kaffeekueche gestartet, sofern nicht ueber die Datei direkt gestartet (if __name__ == "__main__").
    - [BeendenGUIKKT] Hiermit wird die Software fuer die digitale Kaffeekueche beendet.
    - [CheckeLetzteNutzerAktivitaet] Checkt, ob bei Nutzern, die schon lange nicht mehr aktiv waren, ein eingefaerbtes "Zuletzt-Aktiv-Datum" hinzugefuegt werden muss.
    - [CheckeGeburtstage] Checkt, ob die Anzeige von Geburtstagskindern bevorsteht (wenn die Geburtstage innerhalb der Zeitspanne GUI_F1_GeburtstagTage liegen).
    - [CheckeMailStatus] Checkt, ob eine Mail versendet werden darf (je nach Status GUI_F2_MailSchreibenStatus (Ja/Nein) und MailSendenCheck()).
    - [CheckeLogStatus] Checkt, ob eine Woche vergangen ist und schreibt nach dieser Zeitspanne spezielle Logs (z. B. Umsatz der letzten Woche).
    Anmerkung: Weitere Methoden nicht extern aufrufen, da hierfuer nicht gedacht! - Lassen sich hier allerdings auch nicht kapseln (liegt an Gtk.Builder?!).
    """
    def __init__(self):
        # --- GUI: Builder erstellen und anpassen um Widgets aus Glade-Datei auszulesen
        # Builder baut die vorgefertigte GUI auf und ueberfuehrt dies in Python-Code
        builder = Gtk.Builder()
        builder.add_from_file(KKT_Parameter.GUI_F2_GUIElementsDatei)
        builder.connect_signals(self)  # Methoden aus der Glade-Datei mit Methoden weiter unten verbinden

        # --- GUI: Alle Widgets aus der Glade-Datei, die weiter veraendert oder genutzt werden sollen, als Variablen anlegen
        # Die Namen der Objekte sind die Namen, die in der Glade-Datei angelegt wurden
        # Alle Fenster (Windows) und groesseren Container werden angelegt
        self.__WindowTop = builder.get_object("WindowTop")
        self.__ContainerTop = builder.get_object("Container")
        self.__WindowNutzer = builder.get_object("WindowNutzer")
        ViewportNutzer_Kategorie1 = builder.get_object("ViewportNutzer_Kategorie1")
        ViewportNutzer_Kategorie2 = builder.get_object("ViewportNutzer_Kategorie2")
        ViewportNutzer_Kategorie3 = builder.get_object("ViewportNutzer_Kategorie3")
        self.__WindowProgramminfo = builder.get_object("WindowProgramminfo")
        self.__WindowNutzerAnlegen = builder.get_object("WindowNutzerAnlegen")
        ContainerTastatur = builder.get_object("ContainerTastatur")
        self.__WindowNutzerLoeschen = builder.get_object("WindowNutzerLoeschen")
        self.__WindowKontoBestellung = builder.get_object("WindowKontoBestellung")
        ViewportKontoBestellung = builder.get_object("ViewportKontoBestellung")
        self.__WindowKontoAufladen = builder.get_object("WindowKontoAufladen")
        self.__WindowKontoauszug = builder.get_object("WindowKontoauszug")
        self.__ScrolledwindowKontoauszug = builder.get_object("ScrolledwindowKontoauszug")
        self.__WindowBestellabschluss = builder.get_object("WindowBestellabschluss")
        self.__WindowBestellabschlussZins = builder.get_object("WindowBestellabschlussZins")
        self.__ScrolledwindowBestellabschlussZins = builder.get_object("ScrolledwindowZins")
        self.__WindowBestellabschlussStopp = builder.get_object("WindowBestellabschlussStopp")
        self.__WindowBestandAendern = builder.get_object("WindowBestandAendern")
        # Alle benoetigten Labels, Buttons und weiteren Widgets werden angelegt. Namenschema: Label/Button/'NameWidget''NameDesFensters'_'Bezeichnung'
        # Viele Buttons muessen geladen werden, weil nur so die Schrift fett gedruckt werden kann.
        # Labels und Buttons zu Fenster "Nutzer"
        self.__LabelNutzer_Geburtstage = builder.get_object("Nutzer_Geburtstage")
        self.__LabelNutzer_GeburtstageText = builder.get_object("Nutzer_GeburtstageText")
        LabelNutzer_Kategorie1 = builder.get_object("Nutzer_Kategorie1")
        LabelNutzer_Kategorie2 = builder.get_object("Nutzer_Kategorie2")
        LabelNutzer_Kategorie3 = builder.get_object("Nutzer_Kategorie3")
        ButtonNutzer_NutzerAnlegen = builder.get_object("Nutzer_NutzerAnlegen")
        # Labels zu Fenster "Programminfo"
        LabelProgramminfo_GitHub = builder.get_object("Programminfo_GitHub")
        LabelProgramminfo_Version = builder.get_object("Programminfo_Version")
        LabelProgramminfo_Copyright = builder.get_object("Programminfo_Copyright")
        # Labels, Buttons und weitere Widgets zu Fenster "NutzerAnlegen"
        self.__LabelNutzerAnlegen_Geburtstag = builder.get_object("NutzerAnlegen_Geburtstag")
        self.__LabelNutzerAnlegen_Anmerkung = builder.get_object("NutzerAnlegen_Anmerkung")
        self.__ButtonNutzerAnlegen_Kategorie1 = builder.get_object("NutzerAnlegen_Kategorie1")
        ButtonNutzerAnlegen_Kategorie2 = builder.get_object("NutzerAnlegen_Kategorie2")
        ButtonNutzerAnlegen_Kategorie3 = builder.get_object("NutzerAnlegen_Kategorie3")
        ButtonNutzerAnlegen_Hinzufuegen = builder.get_object("NutzerAnlegen_Hinzufuegen")
        ButtonNutzerAnlegen_Zurueck = builder.get_object("NutzerAnlegen_Zurueck")
        self.__EntryNutzerAnlegen_NutzerName = builder.get_object("NutzerAnlegen_NutzerName")
        self.__EntryNutzerAnlegen_BetreuerName = builder.get_object("NutzerAnlegen_BetreuerName")
        self.__EntryNutzerAnlegen_Kalender = builder.get_object("NutzerAnlegen_Kalender")
        # Labels und Buttons zu Fenster "NutzerLoeschen"
        self.__LabelNutzerLoeschen_NutzerName = builder.get_object("NutzerLoeschen_NutzerName")
        self.__LabelNutzerLoeschen_Kontostand = builder.get_object("NutzerLoeschen_Kontostand")
        self.__ButtonNutzerLoeschen_KontostandNullen = builder.get_object("NutzerLoeschen_KontostandNullen")
        ButtonNutzerLoeschen_NEIN = builder.get_object("NutzerLoeschen_NEIN")
        ButtonNutzerLoeschen_JA = builder.get_object("NutzerLoeschen_JA")
        # Labels und Buttons zu Fenster "KontoBestellung"
        self.__LabelKontoBestellung_Kontostand = builder.get_object("KontoBestellung_Kontostand")
        self.__LabelKontoBestellung_NutzerName = builder.get_object("KontoBestellung_NutzerName")
        self.__LabelKontoBestellung_Produktanzahl = builder.get_object("KontoBestellung_Produktanzahl")
        self.__ButtonKontoBestellung_Korrektur = builder.get_object("KontoBestellung_Korrektur")
        self.__ButtonKontoBestellung_DrTitel = builder.get_object("KontoBestellung_DrTitel")
        self.__ButtonKontoBestellung_Kaufen = builder.get_object("KontoBestellung_Kaufen")
        ButtonKontoBestellung_KontoAufladen = builder.get_object("KontoBestellung_KontoAufladen")
        ButtonKontoBestellung_Kontoauszug = builder.get_object("KontoBestellung_Kontoauszug")
        ButtonKontoBestellung_Zurueck = builder.get_object("KontoBestellung_Zurueck")
        # Labels und Buttons zu Fenster "KontoAufladen"
        self.__LabelKontoAufladen_Kontostand = builder.get_object("KontoAufladen_Kontostand")
        self.__LabelKontoAufladen_NutzerName = builder.get_object("KontoAufladen_NutzerName")
        self.__LabelKontoAufladen_Gesamtbetrag = builder.get_object("KontoAufladen_Gesamtbetrag")
        LabelKontoAufladen_Kontodaten = builder.get_object("KontoAufladen_Kontodaten")
        self.__ButtonKontoAufladen_Korrektur = builder.get_object("KontoAufladen_Korrektur")
        self.__ButtonKontoAufladen_Bestaetigen = builder.get_object("KontoAufladen_Bestaetigen")
        ButtonKontoAufladen_Zurueck = builder.get_object("KontoAufladen_Zurueck")
        ButtonKontoAufladen_KontoAufladen = builder.get_object("KontoAufladen_KontoAufladen")
        ButtonKontoAufladen_Kontoauszug = builder.get_object("KontoAufladen_Kontoauszug")
        ButtonKontoAufladen_BetragID1 = builder.get_object("KontoAufladen_BetragID1")
        ButtonKontoAufladen_BetragID2 = builder.get_object("KontoAufladen_BetragID2")
        ButtonKontoAufladen_BetragID3 = builder.get_object("KontoAufladen_BetragID3")
        ButtonKontoAufladen_BetragID4 = builder.get_object("KontoAufladen_BetragID4")
        self.__ButtonKontoAufladen_BetragIDSpuel = builder.get_object("KontoAufladen_BetragIDSpuel")
        # Labels, Buttons und weitere Widgets zu Fenster "Kontoauszug"
        self.__LabelKontoauszug_Kontostand = builder.get_object("Kontoauszug_Kontostand")
        self.__LabelKontoauszug_NutzerName = builder.get_object("Kontoauszug_NutzerName")
        self.__LabelKontoauszug_Datum = builder.get_object("Kontoauszug_Datum")
        self.__LabelKontoauszug_Umsatz = builder.get_object("Kontoauszug_Umsatz")
        LabelKontoauszug_Tage = builder.get_object("Kontoauszug_Tage")
        ButtonKontoauszug_KontoAufladen = builder.get_object("Kontoauszug_KontoAufladen")
        ButtonKontoauszug_Zurueck = builder.get_object("Kontoauszug_Zurueck")
        ButtonKontoauszug_Kontoauszug = builder.get_object("Kontoauszug_Kontoauszug")
        self.__TextViewKontoauszug_Liste = builder.get_object("Kontoauszug_Liste").get_buffer()
        # Labels zu Fenster "Bestellabschluss"
        self.__LabelBestellabschluss_Kontostand = builder.get_object("Bestellabschluss_Kontostand")
        self.__LabelBestellabschluss_Produkte = builder.get_object("Bestellabschluss_Produkte")
        self.__LabelBestellabschluss_Kosten = builder.get_object("Bestellabschluss_Kosten")
        # Labels und Buttons zu Fenster "BestellabschlussZins"
        self.__LabelBestellabschlussZins_Limit = builder.get_object("BestellabschlussZins_Limit")
        self.__LabelBestellabschlussZins_Schulden = builder.get_object("BestellabschlussZins_Schulden")
        self.__LabelBestellabschlussZins_Zinssatz = builder.get_object("BestellabschlussZins_Zinssatz")
        self.__LabelBestellabschlussZins_Zinskosten = builder.get_object("BestellabschlussZins_Zinskosten")
        self.__LabelBestellabschlussZins_Gesamtkosten = builder.get_object("BestellabschlussZins_Gesamtkosten")
        ButtonBestellabschlussZins_Zurueck = builder.get_object("BestellabschlussZins_Zurueck")
        ButtonBestellabschlussZins_Kaufen = builder.get_object("BestellabschlussZins_Kaufen")
        # Labels und Buttons zu Fenster "BestellabschlussStopp"
        self.__LabelBestellabschlussStopp_Limit = builder.get_object("BestellabschlussStopp_Limit")
        self.__LabelBestellabschlussStopp_Schulden = builder.get_object("BestellabschlussStopp_Schulden")
        ButtonBestellabschlussStopp_Zurueck = builder.get_object("BestellabschlussStopp_Zurueck")
        # Labels, Buttons und weitere Widgets zu Fenster "BestandAendern"
        self.__LabelBestandAendern_Produkt = builder.get_object("BestandAendern_Produkt")
        self.__LabelBestandAendern_Bestand = builder.get_object("BestandAendern_Bestand")
        self.__ButtonBestandAendern_Diebstahl = builder.get_object("BestandAendern_Diebstahl")
        self.__ButtonBestandAendern_Bestaetigen = builder.get_object("BestandAendern_Bestaetigen")
        self.__ButtonBestandAendern_Erhoehen = builder.get_object("BestandAendern_Erhoehen")
        ButtonBestandAendern_Reduzieren = builder.get_object("BestandAendern_Reduzieren")
        self.__SpinbuttonBestandAendern_Erhoehen = builder.get_object("SBBestandAendern_Erhoehen")
        self.__SpinbuttonBestandAendern_Reduzieren = builder.get_object("SBBestandAendern_Reduzieren")
        self.__AdjustmentBestandAendern_Erhoehen = builder.get_object("ADBestandAendern_Erhoehen")
        self.__AdjustmentBestandAendern_Reduzieren = builder.get_object("ADBestandAendern_Reduzieren")
        # Weitere benoetigte Widgets werden angelegt. Namenschema: 'NameWidget''NameDesFensters'_'Bezeichnung'
        self.__ImageNutzer_Status = builder.get_object("Nutzer_Status")

        # --- Programmmanagement: Variablen um Einstellungen und Zustaende im Programm verwenden zu koennen
        self.__Datenbank = DBVerwaltung.DBVerwaltung_SQL(KKT_Parameter.GUI_F2_DatenbankDatei)
        self.__ButtonsNutzer = []  # Hier werden die Buttons fuer alle Nutzer gespeichert
        self.__NutzerNeu = {"Name": "", "Kategorie": 0, "Betreuer": "", "Geb": [0, 0, 0]}  # Daten eines neuen Nutzers werden hier zwischengespeichert
        self.__NutzerNamePlatzhalter = "Mustermann"
        self.__ButtonsProdukt = []  # Hier werden die Buttons fuer alle Produkte gespeichert
        self.__ProduktBestand = {}  # Bestand zu jedem Produkt intern gespeichert (alt/aktuell).
        # Z. B. muss so nicht jedes Mal die Datenbank veraendert werden, wenn die Produkte noch nicht gekauft wurden
        self.__Bestellung = []  # Welche Produkte wurden durch den Nutzer ausgewaehlt und sollen gekauft werden
        self.__BestellungKosten = 0  # Wenn der Nutzer Produkte bestellt, werden hier die Kosten zusammengerechnet
        self.__UmsatzWoche = 0  # Hier wird der Umsatz einer Woche gespeichert
        self.__ZeitpunktLogStatus = datetime.today().date()  # Hier wird die letzte Ueberpruefung des LogStatus gespeichert
        self.__ZeitpunktSpuelEingeloest = datetime.today() - timedelta(days=1)  # Hier wird gespeichert, wann die Spuelmaschine das letzte Mal ausgeraeumt wurde
        self.__SpuelEingeloest = False  # Speichert die Einstellung, ob ein Nutzer den Gutschein fuer Spuelmaschine ausraeumen einloesen moechte
        self.__TastaturFokusWidget = None  # Hier wird gespeichert welcher Entry den Fokus hat, um dort mit der Tastatur etwas hineinschreiben zu koennen

        # --- GUI: Anpassungen von Widgets aus der Glade-Datei
        # Fuer Buttons im "NutzerAnlegen"-Fenster wird eine eindeutige ID gesetzt
        self.__ButtonNutzerAnlegen_Kategorie1.set_name("NuID1")
        ButtonNutzerAnlegen_Kategorie2.set_name("NuID2")
        ButtonNutzerAnlegen_Kategorie3.set_name("NuID3")
        # Fuer Buttons im "KontoAufladen"-Fenster wird eine eindeutige ID gesetzt
        ButtonKontoAufladen_BetragID1.set_name("BeID1")
        ButtonKontoAufladen_BetragID2.set_name("BeID2")
        ButtonKontoAufladen_BetragID3.set_name("BeID3")
        ButtonKontoAufladen_BetragID4.set_name("BeID4")
        self.__ButtonKontoAufladen_BetragIDSpuel.set_name("BeIDSpuel")
        # Fuer Buttons im "BestandAendern"-Fenster wird eine eindeutige ID gesetzt
        self.__ButtonBestandAendern_Erhoehen.set_name("IDUp")
        ButtonBestandAendern_Reduzieren.set_name("IDDown")
        # Text von bestimmten Labels direkt zum Start des Programms setzen - z. B. auch Schrift von Labels fett drucken.
        # Entsprechend wird das Label aus der Glade-Datei gelesen und modifiziert und somit wird der Text aus der Glade-Datei ueberschrieben.
        # Mithilfe der "#" (siehe Glade-Datei) wird innerhalb eines Labels markiert, dass eine Ueberschreibung mit einer Variable erfolgen muss.
        # Text von Labels in Fenster "Nutzer" setzen
        LabelNutzer_Kategorie1.set_label("Permanente")
        LabelNutzer_Kategorie2.set_label("Wiss. Mitarbeiter")
        LabelNutzer_Kategorie3.set_label("Studierende")
        ButtonNutzer_NutzerAnlegen.get_child().set_markup("<b>{}</b>".format(ButtonNutzer_NutzerAnlegen.get_child().get_label()))
        # Text von Labels in Fenster "Programminfo" setzen
        LabelProgramminfo_GitHub.set_label(KKT_Parameter.GUI_F3_LinkGitHub)
        TempLabel_Version = LabelProgramminfo_Version.get_label().replace("#", str(KKT_Parameter.GUI_F3_Version) + ", " + KKT_Parameter.GUI_F3_Version_Date, 1)
        LabelProgramminfo_Version.set_label("{}".format(TempLabel_Version))
        LabelProgramminfo_Copyright.set_label("{}".format(LabelProgramminfo_Copyright.get_label().replace("#", str(KKT_Parameter.GUI_F3_Copyright), 1)))
        # Text von Labels in Fenster "NutzerAnlegen" setzen
        self.__ButtonNutzerAnlegen_Kategorie1.get_child().set_markup("<b>{}</b>".format("Permanente"))
        ButtonNutzerAnlegen_Kategorie2.get_child().set_markup("<b>{}</b>".format("Wiss. Mitarbeiter"))
        ButtonNutzerAnlegen_Kategorie3.get_child().set_markup("<b>{}</b>".format("Studierende"))
        ButtonNutzerAnlegen_Zurueck.get_child().set_markup("<b>{}</b>".format(ButtonNutzerAnlegen_Zurueck.get_child().get_label()))
        ButtonNutzerAnlegen_Hinzufuegen.get_child().set_markup("<b>{}</b>".format(ButtonNutzerAnlegen_Hinzufuegen.get_child().get_label()))
        # Text von Labels in Fenster "NutzerLoeschen" setzen
        self.__ButtonNutzerLoeschen_KontostandNullen.get_child().set_markup("<b>{}</b>".format(self.__ButtonNutzerLoeschen_KontostandNullen.get_child().get_label()))
        ButtonNutzerLoeschen_NEIN.get_child().set_markup("<b>{}</b>".format(ButtonNutzerLoeschen_NEIN.get_child().get_label()))
        ButtonNutzerLoeschen_JA.get_child().set_markup("<b>{}</b>".format(ButtonNutzerLoeschen_JA.get_child().get_label()))
        # Text von Labels in Fenster "KontoBestellung" setzen
        self.__LabelKontoBestellung_Produktanzahl.set_label(str(len(self.__Bestellung)))
        self.__ButtonKontoBestellung_Kaufen.get_child().set_markup("<b>{}</b>".format(self.__ButtonKontoBestellung_Kaufen.get_child().get_label()))
        self.__ButtonKontoBestellung_Korrektur.get_child().set_markup("<b>{}</b>".format(self.__ButtonKontoBestellung_Korrektur.get_child().get_label()))
        TempLabel_DrTitel = self.__ButtonKontoBestellung_DrTitel.get_child().get_label().replace("#", str(KKT_Parameter.GUI_F1_DrTitelKosten), 1)
        self.__ButtonKontoBestellung_DrTitel.get_child().set_markup("<b>{}</b>".format(TempLabel_DrTitel))
        ButtonKontoBestellung_KontoAufladen.get_child().set_markup("<b>{}</b>".format(ButtonKontoBestellung_KontoAufladen.get_child().get_label()))
        ButtonKontoBestellung_Zurueck.get_child().set_markup("<b>{}</b>".format(ButtonKontoBestellung_Zurueck.get_child().get_label()))
        ButtonKontoBestellung_Kontoauszug.get_child().set_markup("<b>{}</b>".format(ButtonKontoBestellung_Kontoauszug.get_child().get_label()))
        # Text von Labels in Fenster "KontoAufladen" setzen
        TempLabel_BetragIDSpuel = self.__ButtonKontoAufladen_BetragIDSpuel.get_child().get_label().replace("#", str(KKT_Parameter.GUI_F1_SpuelGutschrift), 1)
        self.__ButtonKontoAufladen_BetragIDSpuel.get_child().set_markup("<b>{}</b>".format(TempLabel_BetragIDSpuel))
        self.__ButtonKontoAufladen_Korrektur.get_child().set_markup("<b>{}</b>".format(self.__ButtonKontoAufladen_Korrektur.get_child().get_label()))
        self.__ButtonKontoAufladen_Bestaetigen.get_child().set_markup("<b>{}</b>".format(self.__ButtonKontoAufladen_Bestaetigen.get_child().get_label()))
        LabelKontoAufladen_Kontodaten.set_label(
            KKT_Parameter.GUI_F1_KontodatenAdmin["Inhaber"] + "\n" + KKT_Parameter.GUI_F1_KontodatenAdmin["IBAN"] + "\n" +
            KKT_Parameter.GUI_F1_KontodatenAdmin["Bankleitzahl"] + "\n" + KKT_Parameter.GUI_F1_KontodatenAdmin["Bankinstitut"])
        ButtonKontoAufladen_Zurueck.get_child().set_markup("<b>{}</b>".format(ButtonKontoAufladen_Zurueck.get_child().get_label()))
        ButtonKontoAufladen_Kontoauszug.get_child().set_markup("<b>{}</b>".format(ButtonKontoAufladen_Kontoauszug.get_child().get_label()))
        ButtonKontoAufladen_BetragID1.get_child().set_markup("<b>{} €</b>".format(KKT_Parameter.GUI_F1_KontoAufladen_Betrag["BeID1"]))
        ButtonKontoAufladen_BetragID2.get_child().set_markup("<b>{} €</b>".format(KKT_Parameter.GUI_F1_KontoAufladen_Betrag["BeID2"]))
        ButtonKontoAufladen_BetragID3.get_child().set_markup("<b>{} €</b>".format(KKT_Parameter.GUI_F1_KontoAufladen_Betrag["BeID3"]))
        ButtonKontoAufladen_BetragID4.get_child().set_markup("<b>{} €</b>".format(KKT_Parameter.GUI_F1_KontoAufladen_Betrag["BeID4"]))
        ButtonKontoAufladen_KontoAufladen.get_child().set_markup("<b>{}</b>".format(ButtonKontoAufladen_KontoAufladen.get_child().get_label()))
        # Text von Labels in Fenster "Kontoauszug" setzen
        LabelKontoauszug_Tage.set_label("{}".format(LabelKontoauszug_Tage.get_label().replace("#", str(KKT_Parameter.GUI_F1_KontoauszugTage), 1)))
        ButtonKontoauszug_KontoAufladen.get_child().set_markup("<b>{}</b>".format(ButtonKontoauszug_KontoAufladen.get_child().get_label()))
        ButtonKontoauszug_Zurueck.get_child().set_markup("<b>{}</b>".format(ButtonKontoauszug_Zurueck.get_child().get_label()))
        ButtonKontoauszug_Kontoauszug.get_child().set_markup("<b>{}</b>".format(ButtonKontoauszug_Kontoauszug.get_child().get_label()))
        # Text von Labels in Fenster "BestellabschlussZins" setzen
        ButtonBestellabschlussZins_Zurueck.get_child().set_markup("<b>{}</b>".format(ButtonBestellabschlussZins_Zurueck.get_child().get_label()))
        ButtonBestellabschlussZins_Kaufen.get_child().set_markup("<b>{}</b>".format(ButtonBestellabschlussZins_Kaufen.get_child().get_label()))
        # Text von Labels in Fenster "BestellabschlussStopp" setzen
        ButtonBestellabschlussStopp_Zurueck.get_child().set_markup("<b>{}</b>".format(ButtonBestellabschlussStopp_Zurueck.get_child().get_label()))
        # Text von Labels in Fenster "BestandAendern" setzen
        self.__ButtonBestandAendern_Erhoehen.get_child().set_markup("<b>{}</b>".format(self.__ButtonBestandAendern_Erhoehen.get_child().get_label()))
        self.__ButtonBestandAendern_Diebstahl.get_child().set_markup("<b>{}</b>".format(self.__ButtonBestandAendern_Diebstahl.get_child().get_label()))
        self.__ButtonBestandAendern_Bestaetigen.get_child().set_markup("<b>{}</b>".format(self.__ButtonBestandAendern_Bestaetigen.get_child().get_label()))
        ButtonBestandAendern_Reduzieren.get_child().set_markup("<b>{}</b>".format(ButtonBestandAendern_Reduzieren.get_child().get_label()))
        # Tastatur implementieren
        Tastatur = GUIElemente.Widget_Tastatur()
        ContainerTastatur.pack_start(Tastatur, False, True, 0)
        Tastatur.connect("TastaturZahl", self.__TastaturZahl)
        Tastatur.connect("TastaturBuchstabe", self.__TastaturZeichen)
        Tastatur.connect("TastaturSonderzeichen", self.__TastaturZeichen)
        Tastatur.connect("TastaturBackspace", self.__TastaturBackspace)
        # Sonstige Anpassungen an GUI-Objekten
        self.__ContainerTop.add(self.__WindowNutzer)
        self.__ContainerTop.add(self.__WindowNutzerAnlegen)
        self.__ContainerTop.add(self.__WindowKontoBestellung)
        self.__ContainerTop.add(self.__WindowBestellabschluss)
        self.__ContainerTop.add(self.__WindowBestellabschlussZins)
        self.__ContainerTop.add(self.__WindowBestellabschlussStopp)
        self.__ContainerTop.add(self.__WindowKontoAufladen)
        self.__ContainerTop.add(self.__WindowKontoauszug)
        self.__WindowProgramminfo.connect("delete-event", self.__delete_event_Programminfo)
        self.__WindowNutzerLoeschen.connect("delete-event", self.__delete_event_NutzerLoeschen)
        self.__WindowBestandAendern.connect("delete-event", self.__delete_event_BestandAendern)
        self.__EntryNutzerAnlegen_NutzerName.connect("focus-in-event", self.__SchreibeTastaturFokusWidget)
        self.__EntryNutzerAnlegen_NutzerName.connect("focus-out-event", self.__SchreibeTastaturFokusWidget)
        self.__EntryNutzerAnlegen_BetreuerName.connect("focus-in-event", self.__SchreibeTastaturFokusWidget)
        self.__EntryNutzerAnlegen_BetreuerName.connect("focus-out-event", self.__SchreibeTastaturFokusWidget)

        # --- GUI: Erweiterung der GUI (aus Glade-Datei) um weitere Widgets
        self.__GridNutzer_Kategorie1 = Gtk.Grid()
        self.__GridNutzer_Kategorie1.set_column_spacing(4)
        self.__GridNutzer_Kategorie1.set_row_spacing(4)
        self.__GridNutzer_Kategorie1.set_column_homogeneous(True)
        self.__GridNutzer_Kategorie2 = Gtk.Grid()
        self.__GridNutzer_Kategorie2.set_column_spacing(4)
        self.__GridNutzer_Kategorie2.set_row_spacing(4)
        self.__GridNutzer_Kategorie2.set_column_homogeneous(True)
        self.__GridNutzer_Kategorie3 = Gtk.Grid()
        self.__GridNutzer_Kategorie3.set_column_spacing(4)
        self.__GridNutzer_Kategorie3.set_row_spacing(4)
        self.__GridNutzer_Kategorie3.set_column_homogeneous(True)
        ViewportNutzer_Kategorie1.add(self.__GridNutzer_Kategorie1)
        ViewportNutzer_Kategorie2.add(self.__GridNutzer_Kategorie2)
        ViewportNutzer_Kategorie3.add(self.__GridNutzer_Kategorie3)
        GridKontoBestellung_Produkt = Gtk.Grid()
        GridKontoBestellung_Produkt.set_column_spacing(10)
        GridKontoBestellung_Produkt.set_row_spacing(6)
        ViewportKontoBestellung.add(GridKontoBestellung_Produkt)

        # --- GUI: Anlegen der Buttons fuer Nutzer und Produkte
        self.__AnlegenButtonsNutzer()
        # Anlegen der Buttons fuer die Produkte
        GridPos = [0, 0]  # Hiermit wird die Position des Buttons in dem GridWidget festgelegt
        for Produkt in self.__Datenbank.LeseAlleZeilen("Bestand"):
            if Produkt[3] == 0:  # Ist das Produkt noch aktiv und wird in der Kaffeekueche angeboten?
                LabelProdukt = Produkt[1] + "\n" + str(Produkt[5]) + " €"
                LabelBestand = "Bestand:  "
                self.__ButtonsProdukt.append(GUIElemente.Widget_Produktanzeige(self.__WindowTop.get_size()[0], self.on_ButtonProdukt_clicked,
                                                                               Produkt[1], LabelProdukt, LabelBestand, Produkt[2],
                                                                               KKT_Parameter.GUI_F2_ButtonProduktPressedZeitspanne))
                self.__ButtonsProdukt[-1].connect("ButtonXsPressed", self.__AnzeigeWindowBestandAendern)
                GridKontoBestellung_Produkt.attach(self.__ButtonsProdukt[-1], GridPos[0], GridPos[1], 1, 1)
                # Nun den Bestand zu jedem Produkt in das dict schreiben
                self.__ProduktBestand.update({Produkt[1]: [Produkt[2], Produkt[2]]})
                if GridPos[0] < 4:
                    GridPos[0] += 1
                else:
                    GridPos[0] = 0
                    GridPos[1] += 1

        # --- Initialisierung der GUI wird nun abgeschlossen
        self.__ThreadFehler = False      # Tritt im Thread (Timer) zur Laufzeit der GUI ein Fehler auf, wechselt diese Variable auf True
        GLib.timeout_add(KKT_Parameter.GUI_F2_VerwaltungInterval * 1000, self.__StarteInterneVerwaltung)
        # Log-Nachricht vorbereiten
        LogNachricht = "Die GUI wurde neu gestartet. Versionsnummer: KKT v{}".format(str(KKT_Parameter.GUI_F3_Version))
        self.__Datenbank.SchreibeNeueZeilen("Log", "zeitpunkt, nachricht", zeitpunkt="datetime('now','localtime')", nachricht=LogNachricht)

        # --- GUI: Anzeige aller Fenster in der GUI auf nicht sichtbar stellen bis auf Uebersicht der Nutzer
        self.__AnzeigeWindowNutzer()
        self.__WindowNutzerAnlegen.hide()
        self.__WindowKontoBestellung.hide()
        self.__WindowBestellabschluss.hide()
        self.__WindowBestellabschlussZins.hide()
        self.__WindowBestellabschlussStopp.hide()
        self.__WindowKontoAufladen.hide()
        self.__WindowKontoauszug.hide()

    # ------------------------- Konstruktor fuer ButtonsNutzer
    # -------------------------------------------------------
    def __AnlegenButtonsNutzer(self):
        """Mit dieser Methode werden die Buttons fuer alle Nutzer angelegt. Die Buttons werden in ein "Grid"-Widget
        einsortiert. Des Weiteren wird die Verknuepfung zwischen den Buttons und der Kontouebersicht zum Bestellen erstellt.
        """
        # Zunaechst werden die alten Buttons zerstoert und die Liste geleert
        if len(self.__ButtonsNutzer) != 0:
            for Button in self.__ButtonsNutzer:
                Button.destroy()
            self.__ButtonsNutzer.clear()
        # Anlegen der Buttons und einsortieren in ein Gitternetz ("Grid"-Widget)
        Counter = 0
        for Kategorie in self.__LeseNutzerNamenAusDatenbank():
            GridPos = [0, 0]  # Hiermit wird die Position des Buttons in dem "Grid"-Widget festgelegt
            for NutzerName in Kategorie:
                self.__ButtonsNutzer.append(GUIElemente.Widget_NutzerButton(self.__WindowTop.get_size()[0],
                                                                            NutzerName, KKT_Parameter.GUI_F2_ButtonNutzerPressedZeitspanne))
                # Bei Nutzern, die schon lange nicht mehr aktiv waren, wird ein eingefaerbtes "Zuletzt-Aktiv"-Datum hinzugefuegt
                NutzerAktivitaet = self.__Datenbank.LeseSpezielleZeilen("Nutzer", 'name="{}"'.format(NutzerName))[0][5]
                NutzerAktivitaetDatumFormatiert = NutzerAktivitaet[:NutzerAktivitaet.find(' ')]
                if not KKT_Verwaltung.ZeitspanneCheckMaxZeitspanne(NutzerAktivitaetDatumFormatiert, KKT_Parameter.GUI_F1_NutzerInaktivTage):
                    self.__ButtonsNutzer[-1].get_child().set_markup("<b>{}</b><span color='#4F5F99'><b>{}</b></span>".format(self.__FormatiereNutzerName(NutzerName),
                                                                                                                             "\n" + NutzerAktivitaetDatumFormatiert))
                else:
                    self.__ButtonsNutzer[-1].get_child().set_markup("<b>{}</b>".format(self.__FormatiereNutzerName(NutzerName)))
                # Weitere Anpassungen des Buttons
                self.__ButtonsNutzer[-1].connect("NutzerButtonXsPressed", self.__AnzeigeWindowNutzerLoeschen)
                self.__ButtonsNutzer[-1].connect("NutzerButtonClicked", self.on_ButtonNutzer_clicked)
                # Einsortieren in ein Gitternetz ("Grid"-Widget)
                if Counter == 0:
                    self.__GridNutzer_Kategorie1.attach(self.__ButtonsNutzer[-1], GridPos[0], GridPos[1], 1, 1)
                elif Counter == 1:
                    self.__GridNutzer_Kategorie2.attach(self.__ButtonsNutzer[-1], GridPos[0], GridPos[1], 1, 1)
                elif Counter == 2:
                    self.__GridNutzer_Kategorie3.attach(self.__ButtonsNutzer[-1], GridPos[0], GridPos[1], 1, 1)
                if GridPos[0] < 4:
                    GridPos[0] += 1
                else:
                    GridPos[0] = 0
                    GridPos[1] += 1
            # Positionen fuer die neue Tab-Seite zuruecksetzen
            GridPos[0] = 0
            GridPos[1] = 0
            Counter += 1

    # --------------- Hauptfunktionen zum MainWindow
    # ---------------------------------------------
    def StartenGUIKKT(self):
        # Hiermit wird die Software fuer die digitale Kaffeekueche gestartet, sofern nicht ueber die Datei direkt gestartet (if __name__ == "__main__").
        self.__WindowTop.show()
        if KKT_Parameter.GUI_F3_Vollbild:
            self.__WindowTop.fullscreen()
        self.__ContainerTop.show()
        Gtk.main()

    def BeendenGUIKKT(self, GUIObjekt, Daten=None):
        # Hiermit wird die Software fuer die digitale Kaffeekueche beendet.
        Gtk.main_quit()

    def __AnzeigeWindowNutzer(self):
        # Zeigt (wieder) das Hauptfenster mit allen Nutzern.
        # Sorgt auch dafuer, dass die Geburtstagsanzeige korrekt funktioniert.
        if self.__LabelNutzer_Geburtstage.get_visible():
            self.__WindowNutzer.show_all()
        else:
            self.__WindowNutzer.show_all()
            self.__LabelNutzer_Geburtstage.set_visible(False)
            self.__LabelNutzer_GeburtstageText.set_visible(False)

    # --------------------------- WindowProgramminfo
    # ---------------------------------------------
    def AnzeigeWindowProgramminfo(self, GUIButton):
        # Wenn der Bediener auf die Statusflaeche im WindowNutzer drueckt, wird diese Methode aufgerufen.
        # Es wird ein neues Fenster WindowProgramminfo geoeffnet
        self.__WindowProgramminfo.show_all()
        self.__WindowProgramminfo.present()

    def __delete_event_Programminfo(self, GUIObjekt, Event):
        # Wenn der Bediener durch "X" das Fenster schliesst, wird diese Methode aufgerufen.
        GUIObjekt.hide()
        return True  # Das muss laut Wiki gemacht werden

    # ------------------------- WindowNutzerAnlegen
    # --------------------------------------------
    def AnzeigeWindowNutzerAnlegen(self, GUIButton):
        # Wenn der Bediener auf den ButtonNutzer_NutzerAnlegen drueckt, wird diese Methode aufgerufen.
        # Damit aendert sich die Anzeige innerhalb des WindowNutzer.
        # Diverse Variablen zuruecksetzen
        self.__ButtonNutzerAnlegen_Kategorie1.set_active(True)
        self.__EntryNutzerAnlegen_NutzerName.set_text("M.  " + self.__NutzerNamePlatzhalter)
        self.__EntryNutzerAnlegen_NutzerName.grab_focus()
        self.__EntryNutzerAnlegen_BetreuerName.set_text("")
        self.__LabelNutzerAnlegen_Geburtstag.set_label("XX.XX.XXXX")
        self.__LabelNutzerAnlegen_Anmerkung.set_label("")
        self.__NutzerNeu["Name"] = ""
        self.__NutzerNeu["Kategorie"] = 0
        self.__NutzerNeu["Betreuer"] = ""
        self.__NutzerNeu["Geb"] = [0, 0, 0]
        # Abschliessen der GUI-Anzeige
        self.__WindowNutzer.hide()
        self.__WindowNutzerAnlegen.show_all()

    def on_ButtonZurueckNutzerAnlegen_clicked(self, GUIButton):
        # Wenn der Bediener auf den ButtonNutzerAnlegen_Zurueck drueckt, wird diese Methode aufgerufen
        self.__WindowNutzerAnlegen.hide()
        self.__AnzeigeWindowNutzer()

    def on_ButtonKategorie_clicked(self, GUIButton):
        # Wenn der Bediener auf einen ButtonNutzerAnlegen_Kategorie drueckt, wird diese Methode aufgerufen.
        if GUIButton.get_active():
            if GUIButton.get_name() == "NuID1":
                self.__NutzerNeu["Kategorie"] = 0
                self.__EntryNutzerAnlegen_BetreuerName.set_can_focus(False)
                self.__EntryNutzerAnlegen_BetreuerName.set_text("")
                self.__LabelNutzerAnlegen_Anmerkung.set_label("")
            if GUIButton.get_name() == "NuID2":
                self.__NutzerNeu["Kategorie"] = 1
                self.__EntryNutzerAnlegen_BetreuerName.set_can_focus(False)
                self.__EntryNutzerAnlegen_BetreuerName.set_text("")
                self.__LabelNutzerAnlegen_Anmerkung.set_label("")
            if GUIButton.get_name() == "NuID3":
                self.__NutzerNeu["Kategorie"] = 2
                self.__EntryNutzerAnlegen_BetreuerName.set_can_focus(True)
                self.__EntryNutzerAnlegen_BetreuerName.set_text(self.__NutzerNamePlatzhalter)
                self.__EntryNutzerAnlegen_BetreuerName.grab_focus()  # Nur bei Studi muss und darf ein Betreuer angegeben werden
                self.__LabelNutzerAnlegen_Anmerkung.set_label("Anmerkung: Betreuer angeben.")

    def on_CalenderDate_changed(self, GUIObjekt):
        # Wenn der Bediener ein Datum im Kalender auswaehlt, wird diese Methode aufgerufen.
        Counter = 0
        for DateObject in reversed(self.__EntryNutzerAnlegen_Kalender.get_date()):
            if Counter == 1:
                self.__NutzerNeu["Geb"][Counter] = DateObject + 1
            else:
                self.__NutzerNeu["Geb"][Counter] = DateObject
            Counter += 1
        LabelDate = str(self.__NutzerNeu["Geb"])[1:-1].replace(", ", ".")
        self.__LabelNutzerAnlegen_Geburtstag.set_label(LabelDate)  # Der Geburtstag wird angezeigt

    def on_ButtonHinzufuegen_clicked(self, GUIButton):
        # Wenn der Bediener auf den ButtonNutzerAnlegen_Hinzufuegen drueckt, wird diese Methode aufgerufen.
        # Zunaechst werden die Eingaben ueberprueft und erst dann der neue Nutzer akzeptiert. Bei fehlerhaften Eingaben wird kein Nutzer angelegt.
        AngabenKorrekt = False
        if len(self.__EntryNutzerAnlegen_NutzerName.get_text()) <= 3:
            # Zu kurze Namen werden nicht akzeptiert
            self.__EntryNutzerAnlegen_NutzerName.set_text("")
            self.__EntryNutzerAnlegen_NutzerName.grab_focus()
            self.__LabelNutzerAnlegen_Anmerkung.set_label("Anmerkung: Name zu kurz.")
        elif self.__EntryNutzerAnlegen_NutzerName.get_text().find(self.__NutzerNamePlatzhalter) != -1:
            # Mustermann als Name wird nicht akzeptiert
            self.__EntryNutzerAnlegen_NutzerName.set_text("")
            self.__EntryNutzerAnlegen_NutzerName.grab_focus()
            self.__LabelNutzerAnlegen_Anmerkung.set_label("Anmerkung: Name Mustermann nicht akzeptiert.")
        else:
            # Pruefen, ob es den Namen schon in der Datenbank gibt
            NutzerNameVergeben = False
            for Kategorie in self.__LeseNutzerNamenAusDatenbank():
                for NutzerName in Kategorie:
                    if NutzerName.find(self.__EntryNutzerAnlegen_NutzerName.get_text()) != -1:
                        NutzerNameVergeben = True
                        self.__LabelNutzerAnlegen_Anmerkung.set_label("Anmerkung: Der Name existiert schon.")
                        break
            if not NutzerNameVergeben:
                # Bei Studenten wird ueberprueft, ob der angegebene Betreuer existiert
                if self.__EntryNutzerAnlegen_BetreuerName.get_can_focus():  # Wenn man Studi ausgewaehlt hat, ist das erfuellt
                    if len(self.__EntryNutzerAnlegen_BetreuerName.get_text()) <= 2 or not self.__EntryNutzerAnlegen_BetreuerName.get_text()[:1].isupper():
                        self.__EntryNutzerAnlegen_BetreuerName.set_text("")
                        self.__EntryNutzerAnlegen_BetreuerName.grab_focus()
                        self.__LabelNutzerAnlegen_Anmerkung.set_label("Anmerkung: Betreuer existiert nicht.")
                    else:  # Nun wird ueberprueft, ob es den Betreuer ueberhaupt gibt
                        BetreuerExistiert = False
                        CounterKategorie = 0
                        for Kategorie in self.__LeseNutzerNamenAusDatenbank():
                            if CounterKategorie == 2: break
                            for NutzerName in Kategorie:
                                if NutzerName.find(self.__EntryNutzerAnlegen_BetreuerName.get_text()) != -1:
                                    BetreuerExistiert = True
                                    break
                            CounterKategorie += 1
                        if BetreuerExistiert:  # Namen speichern
                            AngabenKorrekt = True
                        else:
                            self.__EntryNutzerAnlegen_BetreuerName.set_text("")
                            self.__EntryNutzerAnlegen_BetreuerName.grab_focus()
                            self.__LabelNutzerAnlegen_Anmerkung.set_label("Anmerkung: Betreuer existiert nicht.")
                else:
                    AngabenKorrekt = True
        # Nutzer anlegen, sofern die Eingaben nicht fehlerhaft sind.
        if AngabenKorrekt:
            self.__NutzerNeu["Name"] = self.__VereinheitlicheNutzerName(self.__EntryNutzerAnlegen_NutzerName.get_text())
            Geburtstag = ""
            if not self.__NutzerNeu["Geb"][0] == 0:  # Wenn ein Geburtstag uebergeben wurde
                Geburtstag = str(self.__NutzerNeu["Geb"])[1:-1].replace(", ", ".")
            if self.__EntryNutzerAnlegen_BetreuerName.get_can_focus():  # Wenn die Kategorie Studierende ausgewaehlt wurde, dann ist das erfuellt
                self.__NutzerNeu["Betreuer"] = "[" + self.__EntryNutzerAnlegen_BetreuerName.get_text() + "]"
                self.__Datenbank.SchreibeNeueZeilen("Nutzer", "name, kontostand, rang, Geburtstag, LetzteAktivitaet",
                                                    name=self.__NutzerNeu["Name"] + " " + self.__NutzerNeu["Betreuer"], kontostand=0,
                                                    rang=self.__NutzerNeu["Kategorie"], Geburtstag=Geburtstag, LetzteAktivitaet="datetime('now','localtime')")
            else:
                self.__Datenbank.SchreibeNeueZeilen("Nutzer", "name, kontostand, rang, Geburtstag, LetzteAktivitaet",
                                                    name=self.__NutzerNeu["Name"], kontostand=0,
                                                    rang=self.__NutzerNeu["Kategorie"], Geburtstag=Geburtstag, LetzteAktivitaet="datetime('now','localtime')")
            # Log-Nachricht vorbereiten
            LogNachricht = "Neuer Nutzer angelegt: " + str(self.__NutzerNeu)
            self.__Datenbank.SchreibeNeueZeilen("Log", "zeitpunkt, nachricht", zeitpunkt="datetime('now','localtime')", nachricht=LogNachricht)
            # Abschliessen der GUI-Anzeige
            # Anmerkung: Alle Variablen zum "Nutzer anlegen" usw. werden zurueckgesetzt, wenn ein Klick auf ButtonNutzer_NutzerAnlegen erfolgt
            self.__AnlegenButtonsNutzer()  # Neuer Name im System und damit muessen die Buttons aktualisiert werden
            self.__WindowNutzerAnlegen.hide()
            self.__AnzeigeWindowNutzer()

    def __SchreibeTastaturFokusWidget(self, GUIWidget, Event):
        # Es wird in die interne Variable TastaturFokusWidget geschrieben, welcher Entry gerade den Fokus besitzt.
        # Hierdurch kann bestimmt werden, in welchen Entry die Tastatur schreiben kann.
        if Event.in_:
            self.__TastaturFokusWidget = GUIWidget
        else:   # Fuer focus-out-event
            if self.__TastaturFokusWidget is GUIWidget:
                self.__TastaturFokusWidget = None

    def __TastaturZeichen(self, GUIButton, Zeichen):
        # Tastatureingaben weiterleiten
        self.__SchreibeInEntry(Zeichen)

    def __TastaturZahl(self, GUIButton, Zahl):
        # Tastatureingaben weiterleiten
        self.__SchreibeInEntry(str(Zahl))

    def __TastaturBackspace(self, GUIButton):
        # Tastatureingaben weiterleiten
        self.__LoescheAusEntry()

    def __SchreibeInEntry(self, Zeichen):
        # Schreibt das uebergebene Zeichen in ein EntryObjekt
        if self.__TastaturFokusWidget is not None:
            if self.__TastaturFokusWidget.props.cursor_position != self.__TastaturFokusWidget.props.selection_bound:
                self.__LoescheAusEntry()
            CursorPosition = self.__TastaturFokusWidget.props.cursor_position
            TextNeu = self.__TastaturFokusWidget.get_text()[:CursorPosition] + Zeichen + self.__TastaturFokusWidget.get_text()[CursorPosition:]
            self.__TastaturFokusWidget.set_text(TextNeu)
            self.__TastaturFokusWidget.set_position(CursorPosition + 1)

    def __LoescheAusEntry(self):
        # Loescht ein Zeichen an der aktuellen Position des Cursors oder eine ausgewaehlte Zeichenfolge aus einem EntryObjekt
        if self.__TastaturFokusWidget is not None:
            CursorPosition = self.__TastaturFokusWidget.props.cursor_position
            SelectionPosition = self.__TastaturFokusWidget.props.selection_bound  # Ist auf der gegenueberliegenden Seite zur CursorPosition
            if CursorPosition != 0 and CursorPosition == SelectionPosition:
                TextNeu = self.__TastaturFokusWidget.get_text()[:CursorPosition - 1] + self.__TastaturFokusWidget.get_text()[CursorPosition:]
                self.__TastaturFokusWidget.set_text(TextNeu)
                self.__TastaturFokusWidget.set_position(CursorPosition - 1)
            elif CursorPosition != SelectionPosition:
                if CursorPosition < SelectionPosition:
                    TextNeu = self.__TastaturFokusWidget.get_text()[:CursorPosition] + self.__TastaturFokusWidget.get_text()[SelectionPosition:]
                    self.__TastaturFokusWidget.set_text(TextNeu)
                    self.__TastaturFokusWidget.set_position(CursorPosition)
                else:
                    TextNeu = self.__TastaturFokusWidget.get_text()[:SelectionPosition] + self.__TastaturFokusWidget.get_text()[CursorPosition:]
                    self.__TastaturFokusWidget.set_text(TextNeu)
                    self.__TastaturFokusWidget.set_position(SelectionPosition)

    # ------------------------- WindowNutzerLoeschen
    # ---------------------------------------------
    def __AnzeigeWindowNutzerLoeschen(self, GUIButton):
        # Wenn der Bediener den Button eines Nutzers fuer die festgelegte Zeitspanne drueckt, wird ein neues Fenster geoeffnet.
        # Siehe Zeitspanne GUI_F2_ButtonNutzerPressedZeitspanne
        self.__LabelNutzerLoeschen_NutzerName.set_label(GUIButton.LeseID())
        self.__ButtonNutzerLoeschen_KontostandNullen.set_active(False)
        Kontostand = self.__Datenbank.LeseSpezielleZeilen("Nutzer", 'name="{}"'.format(GUIButton.LeseID()))[0][2]
        if Kontostand < 0.0:
            self.__LabelNutzerLoeschen_Kontostand.set_markup("<span color='red'>{} €</span>".format(str(Kontostand)))
        else:
            self.__LabelNutzerLoeschen_Kontostand.set_label(str(Kontostand) + " €")
        self.__WindowNutzerLoeschen.show_all()
        self.__WindowNutzerLoeschen.present()

    def on_ButtonJA_clicked(self, GUIButton):
        NutzerName = self.__LabelNutzerLoeschen_NutzerName.get_label()
        # Zunaechst wird der zu loeschende Nutzer zur Archivierung in eine Datenbank fuer Ehemalige abgelegt.
        # Der Geburtstag wird dem Datenschutz zuliebe geloescht. Die letzte Aktivitaet ist ebenso nicht mehr relevant.
        NutzerDaten = self.__Datenbank.LeseSpezielleZeilen("Nutzer", 'name="{}"'.format(NutzerName))[0]
        if self.__ButtonNutzerLoeschen_KontostandNullen.get_active():
            self.__Datenbank.SchreibeNeueZeilen("NutzerAlt", "name, kontostand, rang", name=NutzerDaten[1], kontostand=0, rang=NutzerDaten[3])
        else:
            self.__Datenbank.SchreibeNeueZeilen("NutzerAlt", "name, kontostand, rang", name=NutzerDaten[1], kontostand=NutzerDaten[2], rang=NutzerDaten[3])
        # Nun wird der Nutzer aus der aktiven Datenbank geloescht
        self.__Datenbank.LoescheSpezielleZeile("Nutzer", 'name="{}"'.format(NutzerName))
        # Log-Nachricht vorbereiten
        if self.__ButtonNutzerLoeschen_KontostandNullen.get_active():
            LogNachricht = "Der Nutzer '{}' wurde geloescht und der Kontostand auf Null gesetzt".format(NutzerName)
        else:
            LogNachricht = "Der Nutzer '{}' wurde geloescht".format(NutzerName)
        self.__Datenbank.SchreibeNeueZeilen("Log", "zeitpunkt, nachricht", zeitpunkt="datetime('now','localtime')", nachricht=LogNachricht)
        # Abschliessen der GUI-Anzeige
        # Buttons fuer alle Nutzer muessen neu erstellt werden, weil ein Nutzer entfernt wurde.
        self.__AnlegenButtonsNutzer()
        self.__WindowNutzerLoeschen.hide()
        self.__AnzeigeWindowNutzer()

    def on_ButtonNEIN_clicked(self, GUIButton):
        self.__WindowNutzerLoeschen.hide()

    def __delete_event_NutzerLoeschen(self, GUIObjekt, Event):
        # Wenn der Bediener durch "X" das Fenster schliesst, wird diese Methode aufgerufen.
        GUIObjekt.hide()
        return True  # Das muss laut Wiki gemacht werden

    # ------------------------- WindowKontoBestellung
    # ----------------------------------------------
    def on_ButtonNutzer_clicked(self, GUIButton):
        # Wenn der Bediener auf den Button eines Nutzer drueckt, wird diese Methode aufgerufen
        # NutzerName in Labels schreiben und Kontostand des Nutzers aktualisieren
        self.__LabelKontoBestellung_NutzerName.set_label(GUIButton.LeseID())
        self.__LabelKontoAufladen_NutzerName.set_label(GUIButton.LeseID())
        self.__LabelKontoauszug_NutzerName.set_label(GUIButton.LeseID())
        self.__AktualisiereLabelKontostand()
        # Interne Listen mit Datenbank abgleichen, damit GUI und Datenbank auf jeden Fall synchron sind
        for Button in self.__ButtonsProdukt:
            Bestand = self.__Datenbank.LeseSpezielleZeilen("Bestand", 'produkt="{}"'.format(Button.LeseID()))[0][2]
            Button.AnpassenLabelUnterButton(Bestand)
            self.__ProduktBestand[Button.LeseID()][0] = Bestand
            self.__ProduktBestand[Button.LeseID()][1] = Bestand
        # Abschliessen der GUI-Anzeige und zuruecksetzen von Variablen etc.
        self.__ButtonKontoBestellung_DrTitel.set_sensitive(True)
        self.__ButtonKontoBestellung_Kaufen.set_sensitive(False)
        self.__ButtonKontoBestellung_Korrektur.set_sensitive(False)
        self.__LabelKontoBestellung_Produktanzahl.set_label("0")
        self.__Bestellung.clear()
        self.__BestellungKosten = 0
        self.__WindowNutzer.hide()
        self.__WindowKontoBestellung.show_all()

    def on_ButtonZurueck_clicked(self, GUIButton):
        # Wenn der Bediener auf den ButtonKontoBestellung_Zurueck drueckt, wird diese Methode aufgerufen
        # Wenn dieser Button gedrueckt wird, dann wird automatisch auch "on_korrektur_clicked" ausgefuehrt. Steht in Glade-Datei!
        self.__WindowKontoBestellung.hide()
        self.__AnzeigeWindowNutzer()

    def on_ButtonKorrektur_clicked(self, GUIButton):
        # Wenn der Bediener auf den ButtonKontoBestellung_Korrektur drueckt, wird diese Methode aufgerufen
        # Zuruecksetzen von Variablen etc.
        self.__ButtonKontoBestellung_DrTitel.set_sensitive(True)
        self.__ButtonKontoBestellung_Kaufen.set_sensitive(False)
        self.__ButtonKontoBestellung_Korrektur.set_sensitive(False)
        self.__LabelKontoBestellung_Produktanzahl.set_label("0")
        self.__Bestellung.clear()
        self.__BestellungKosten = 0
        # Zuruecksetzen der Bestandsanzeige unter den Produktbuttons und zuruecksetzen der Bestands-Variable
        for Button in self.__ButtonsProdukt:
            Button.AnpassenLabelUnterButton(self.__ProduktBestand[Button.LeseID()][0])
            self.__ProduktBestand[Button.LeseID()][1] = self.__ProduktBestand[Button.LeseID()][0]

    def on_ButtonDrTitel_clicked(self, GUIButton):
        # Wenn der Bediener auf den ButtonKontoBestellung_DrTitel drueckt, wird diese Methode aufgerufen
        if "Dr.-Titel" not in self.__Bestellung:
            self.__Bestellung.append("Dr.-Titel")
            self.__LabelKontoBestellung_Produktanzahl.set_label(str(len(self.__Bestellung)))
        self.__ButtonKontoBestellung_DrTitel.set_sensitive(False)
        self.__ButtonKontoBestellung_Kaufen.set_sensitive(True)
        self.__ButtonKontoBestellung_Korrektur.set_sensitive(True)
        self.__BestellungKosten += KKT_Parameter.GUI_F1_DrTitelKosten

    def on_ButtonProdukt_clicked(self, GUIButton, GUIWidget):
        # Wenn der Bediener auf einen Button fuer ein Produkt drueckt, wird diese Methode aufgerufen
        if self.__ProduktBestand[GUIWidget.LeseID()][1] > 0:  # Produkt wird nur in die Bestellliste aufgenommen, wenn der Bestand noch nicht auf Null gefallen ist
            # Das ausgewaehlte Produkt wird in die Liste der Bestellungen geschrieben
            self.__Bestellung.append(GUIWidget.LeseID())
            # Die Kosten aller ausgewaehlten Produkte werden zusammengerechnet
            self.__BestellungKosten += self.__Datenbank.LeseSpezielleZeilen("Bestand", 'produkt="{}"'.format(GUIWidget.LeseID()))[0][5]
            # Unten in der GUI wird die bestellte Anzahl an Produkten angezeigt
            self.__LabelKontoBestellung_Produktanzahl.set_label(str(len(self.__Bestellung)))
            # Der Bestand wird intern angepasst
            self.__ProduktBestand[GUIWidget.LeseID()][1] -= 1
            GUIWidget.AnpassenLabelUnterButton(self.__ProduktBestand[GUIWidget.LeseID()][1])
            # Abschliessen der GUI-Anzeige
            self.__ButtonKontoBestellung_Kaufen.set_sensitive(True)
            self.__ButtonKontoBestellung_Korrektur.set_sensitive(True)
        else:  # Blinkeffekt, um den Nutzer darauf hinzuweisen, dass das Produkt ausverkauft ist
            GUIWidget.BlinkenLabelUnterButton()

    def on_ButtonKaufen_clicked(self, GUIButton):
        # Wenn der Bediener auf den ButtonKontoBestellung_Kaufen drueckt, wird diese Methode aufgerufen
        # Es wird vor dem Kauf ueberprueft, ob der Nutzer schon zu große Schuldenberge aufgetuermt hat
        Kontostand = self.__Datenbank.LeseSpezielleZeilen("Nutzer", 'name="{}"'.format(self.__LabelKontoBestellung_NutzerName.get_label()))[0][2]
        if Kontostand <= KKT_Parameter.GUI_F1_MaxSchulden:
            # Abschliessen der GUI-Anzeige
            TempLabel_Limit = self.__LabelBestellabschlussStopp_Limit.get_label().replace("#", str(round(KKT_Parameter.GUI_F1_MaxSchulden, 2)), 1)
            self.__LabelBestellabschlussStopp_Limit.set_label("{}".format(TempLabel_Limit))
            self.__LabelBestellabschlussStopp_Schulden.set_markup("<span color='red'>{}</span>".format(Kontostand))
            self.__WindowKontoBestellung.hide()
            self.__WindowBestellabschlussStopp.show_all()
        elif Kontostand <= KKT_Parameter.GUI_F1_MaxSchulden * (2 / 3):
            # Berechnen von Zinssatz und Zinskosten, da Schuldenberg zu gross und normales Kaufen nicht mehr gewuenscht
            Parameter_a = 0.1
            Parameter_b = np.log(2.5/0.1)
            Skalentransformation = (Kontostand - KKT_Parameter.GUI_F1_MaxSchulden * (2 / 3)) / \
                                   (KKT_Parameter.GUI_F1_MaxSchulden - KKT_Parameter.GUI_F1_MaxSchulden * (2 / 3))
            Zinssatz = round(Parameter_a * np.exp(Parameter_b * Skalentransformation), 3)
            Zinskosten = round((Zinssatz/100) * abs(Kontostand), 3)
            self.__BestellungKosten = round(self.__BestellungKosten + Zinskosten, 2)
            # Zeichnen des Zinsgraphen
            Graph = Figure()
            Graph.subplots_adjust(left=0.20, bottom=0.19, right=0.97, top=0.96)
            GraphIntern = Graph.add_subplot(111)
            Intervall = np.arange(round(abs(KKT_Parameter.GUI_F1_MaxSchulden) * (2 / 3), 0), round(abs(KKT_Parameter.GUI_F1_MaxSchulden) + 1, 0), 1)
            Intervall_Skalentransformation = (-Intervall - KKT_Parameter.GUI_F1_MaxSchulden * (2 / 3)) / \
                                             (KKT_Parameter.GUI_F1_MaxSchulden - KKT_Parameter.GUI_F1_MaxSchulden * (2 / 3))
            Zinsfunktion = Parameter_a * np.exp(Parameter_b * Intervall_Skalentransformation)
            GraphIntern.set_xlabel('Schulden in €')
            GraphIntern.set_ylabel('Zinssatz in %')
            GraphIntern.set_yticks(np.arange(0, 3, 0.25))
            GraphIntern.grid(axis='both', linestyle='--', linewidth=0.5)
            GraphIntern.plot(Intervall, Zinsfunktion, 'k')
            GraphIntern.plot(abs(Kontostand), Zinssatz, 'ro')
            # Einbinden des Zinsgraphen in PyGTK
            if len(self.__ScrolledwindowBestellabschlussZins.get_children()) > 0:   # Sonst kann der Graph nicht neu gezeichnet werden
                self.__ScrolledwindowBestellabschlussZins.get_children()[0].destroy()
            self.__ScrolledwindowBestellabschlussZins.add(FigureCanvas(Graph))
            # Abschliessen der GUI-Anzeige
            TempLabel_Limit = self.__LabelBestellabschlussZins_Limit.get_label().replace("#", str(round(KKT_Parameter.GUI_F1_MaxSchulden * (2 / 3), 2)), 1)
            self.__LabelBestellabschlussZins_Limit.set_label("{}".format(TempLabel_Limit))
            self.__LabelBestellabschlussZins_Schulden.set_markup("<span color='red'>{}</span>".format(Kontostand))
            self.__LabelBestellabschlussZins_Zinssatz.set_label("{}".format(Zinssatz))
            self.__LabelBestellabschlussZins_Zinskosten.set_label("{}".format(Zinskosten))
            self.__LabelBestellabschlussZins_Gesamtkosten.set_label("{}".format(self.__BestellungKosten))
            self.__WindowKontoBestellung.hide()
            self.__WindowBestellabschlussZins.show_all()
        else:
            self.__WindowKontoBestellung.hide()
            self.__BestellungAbschliessen()

    # ------------------------- WindowBestellabschlussZins
    # ---------------------------------------------------
    def on_ButtonKaufenZins_clicked(self, GUIButton):
        # Wenn der Bediener auf den ButtonBestellabschlussZins_Kaufen drueckt, wird diese Methode aufgerufen
        self.__WindowBestellabschlussZins.hide()
        self.__BestellungAbschliessen()

    def on_ButtonZurueckZins_clicked(self, GUIButton):
        # Wenn der Bediener auf den ButtonBestellabschlussZins_Zurueck drueckt, wird diese Methode aufgerufen
        # Wenn dieser Button gedrueckt wird, dann wird automatisch auch "on_korrektur_clicked" ausgefuehrt. Steht in Glade-Datei!
        self.__WindowBestellabschlussZins.hide()
        self.__WindowKontoBestellung.show_all()

    # ------------------------- WindowBestellabschlussStopp
    # ----------------------------------------------------
    def on_ButtonZurueckStopp_clicked(self, GUIButton):
        # Wenn der Bediener auf den ButtonBestellabschlussStopp_Zurueck drueckt, wird diese Methode aufgerufen
        # Wenn dieser Button gedrueckt wird, dann wird automatisch auch "on_korrektur_clicked" ausgefuehrt. Steht in Glade-Datei!
        self.__WindowBestellabschlussStopp.hide()
        self.__WindowKontoBestellung.show_all()

    # --------- Interne Funktionen fuer Bestellung abschliessen
    # --------------------------------------------------------
    def __BestellungAbschliessen(self):
        # Bestellung wird abgeschlossen, indem Kosten verrechnet und Daten in die Datenbank geschrieben werden
        self.__BestellungKosten = round(self.__BestellungKosten, 3)  # Es kam mal zu einem seltsamen Bug, dass sehr viele Nachkommastellen angegeben wurden
        self.__UmsatzWoche += self.__BestellungKosten
        # Kontostand anpassen und in die Datenbank schreiben
        Kontostand = self.__Datenbank.LeseSpezielleZeilen("Nutzer", 'name="{}"'.format(self.__LabelKontoBestellung_NutzerName.get_label()))[0][2]
        KontostandNeu = round(Kontostand - self.__BestellungKosten, 3)
        self.__Datenbank.UeberschreibeZeile("Nutzer", 'name="{}"'.format(self.__LabelKontoBestellung_NutzerName.get_label()), kontostand=KontostandNeu)
        # Bestand in der Datenbank aktualisieren
        for Produkt, Anzahl in self.__ProduktBestand.items():
            self.__Datenbank.UeberschreibeZeile("Bestand", 'produkt="{}"'.format(Produkt), anzahl=Anzahl[1])
        # Die Bestellungen werden in der Datenbank geloggt. Fuer jedes Produkt eine eigene Zeile in der Datenbank
        for Produkt in self.__Bestellung:
            self.__Datenbank.SchreibeNeueZeilen("Bestellung", "zeitpunkt, produkt, name", zeitpunkt="datetime('now','localtime')",
                                                produkt=Produkt, name=self.__LabelKontoBestellung_NutzerName.get_label())
        # Die Aktivitaet des Nutzers in der Datenbank neu setzen
        self.__Datenbank.UeberschreibeZeile("Nutzer", 'name="{}"'.format(self.__LabelKontoBestellung_NutzerName.get_label()),
                                            LetzteAktivitaet="datetime('now','localtime')")
        # Der Doktortitel wird dem NutzerNamen in der Datenbank und dem Button hinzugefuegt (sofern gekauft)
        if "Dr.-Titel" in self.__Bestellung:
            NutzerNameNeu = self.__FormatiereNutzerNameDrTitel(self.__LabelKontoBestellung_NutzerName.get_label())
            self.__AktualisiereButtonNutzer(self.__LabelKontoBestellung_NutzerName.get_label(), NutzerNameNeu)  # Aktualisiert gleichzeitig die Datenbank
            # Log-Nachricht vorbereiten, dass Nutzer einen Doktortitel gekauft hat
            LogNachricht = "Der Nutzer {} hat einen Doktortitel (Dr.) gekauft".format(self.__LabelKontoBestellung_NutzerName.get_label())
            self.__Datenbank.SchreibeNeueZeilen("Log", "zeitpunkt, nachricht", zeitpunkt="datetime('now','localtime')", nachricht=LogNachricht)
        else:
            # Wenn der NutzerName nicht durch einen Doktortitel-Kauf geandert wird, muss noch die Aktivitaet des Nutzers auf dem Button angepasst werden
            self.__AktualisiereButtonNutzerAktivitaet(self.__LabelKontoBestellung_NutzerName.get_label())
        # Die GUI-Anzeige wechselt auf eine Uebersichtsanzeige
        self.__LabelBestellabschluss_Kosten.set_markup("<span color='red'>{}</span>".format(str(self.__BestellungKosten)))
        if KontostandNeu <= KKT_Parameter.GUI_F1_MaxSchulden/3:
            self.__LabelBestellabschluss_Kontostand.set_markup("<span color='red'>{} €</span>".format(str(KontostandNeu)))
        else:
            self.__LabelBestellabschluss_Kontostand.set_label(str(KontostandNeu) + " €")
        # Die gekauften Produkte werden aufgelistet
        AuflistungProdukte = "Gekaufte Produkte:\n\n"
        ProdukteGebuendelt = []
        for Produkt in self.__Bestellung:
            if Produkt not in ProdukteGebuendelt:
                AuflistungProdukte += " - " + str(self.__Bestellung.count(Produkt)) + "x " + Produkt + "\n"
                ProdukteGebuendelt.append(Produkt)
        self.__LabelBestellabschluss_Produkte.set_label(AuflistungProdukte)
        # Abschliessen der GUI-Anzeige
        self.__WindowBestellabschluss.show_all()
        GLib.timeout_add(KKT_Parameter.GUI_F2_BestellabschlussZeitspanne * 1000, self.__BestellungAbschliessenEnde)
        # Anmerkung: Alle Variablen zum Bestand usw. werden zurueckgesetzt, wenn ein Klick auf einen Button eines Nutzers erfolgt
        # Demnach muessen diese hier nicht zurueckgesetzt werden

    def __BestellungAbschliessenEnde(self):
        # Wird nach dem Abschluss des Kaufs ausgefuehrt. Damit geht die GUI-Anzeige wieder auf die Startseite mit den Buttons der Nutzer
        self.__WindowBestellabschluss.hide()
        self.__AnzeigeWindowNutzer()
        return False  # Ohne diese Zeile wird der GLib-Timer immer wieder ausgefuehrt

    # ------------------------- WindowKontoAufladen
    # --------------------------------------------
    def AnzeigeWindowKontoAufladen(self, GUIButton):
        # Wenn der Bediener auf den ButtonKontoBestellung_KontoAufladen oder ButtonKontoauszug_KontoAufladen drueckt, wird diese Methode aufgerufen.
        # Es aendert sich die Anzeige innerhalb des ButtonKontoBestellung oder WindowKontoauszug
        self.__ResetWindowKontoAufladen()
        self.__WindowKontoBestellung.hide()
        self.__WindowKontoauszug.hide()
        self.__WindowKontoAufladen.show_all()

    def on_ButtonZurueckKontoAufladen_clicked(self, GUIButton):
        # Wenn der Bediener auf den ButtonKontoAufladen_Zurueck drueckt, wird diese Methode aufgerufen.
        # Damit geht die Anzeige wieder zurueck zum WindowKontoBestellung
        self.__WindowKontoAufladen.hide()
        self.__WindowKontoBestellung.show_all()

    def on_ButtonBetragID_clicked(self, GUIButton):
        # Wenn der Bediener auf einen ButtonKontoAufladen_BetragID drueckt, wird diese Methode aufgerufen.
        self.__ButtonKontoAufladen_Bestaetigen.set_sensitive(True)
        self.__ButtonKontoAufladen_Korrektur.set_sensitive(True)
        if GUIButton.get_name() == "BeIDSpuel":
            GUIButton.set_sensitive(False)
            self.__SpuelEingeloest = True
            self.__LabelKontoAufladen_Gesamtbetrag.set_label(str(float(self.__LabelKontoAufladen_Gesamtbetrag.get_label()) +
                                                                 float(KKT_Parameter.GUI_F1_SpuelGutschrift)))
        else:
            Betrag = KKT_Parameter.GUI_F1_KontoAufladen_Betrag[GUIButton.get_name()]
            self.__LabelKontoAufladen_Gesamtbetrag.set_label(str(float(self.__LabelKontoAufladen_Gesamtbetrag.get_label()) + float(Betrag)))

    def on_ButtonKorrekturKontoAufladen_clicked(self, GUIButton):
        # Wenn der Bediener auf den ButtonKontoAufladen_Korrektur drueckt, wird diese Methode aufgerufen.
        self.__ResetWindowKontoAufladen()

    def on_ButtonBestaetigen_clicked(self, GUIButton):
        # Wenn der Bediener auf den ButtonKontoAufladen_Bestaetigen drueckt, wird diese Methode aufgerufen.
        # Auslesen des aktuellen Kontostands, neuen Kontostand bestimmen und danach in Datenbank schreiben.
        Kontostand = self.__Datenbank.LeseSpezielleZeilen("Nutzer", 'name="{}"'.format(self.__LabelKontoBestellung_NutzerName.get_label()))[0][2]
        KontostandNeu = round(Kontostand + float(self.__LabelKontoAufladen_Gesamtbetrag.get_label()), 3)
        self.__Datenbank.UeberschreibeZeile("Nutzer", 'name="{}"'.format(self.__LabelKontoBestellung_NutzerName.get_label()), kontostand=KontostandNeu)
        # Die Aktivitaet des Nutzers in Datenbank neu setzen
        self.__Datenbank.UeberschreibeZeile("Nutzer", 'name="{}"'.format(self.__LabelKontoBestellung_NutzerName.get_label()),
                                            LetzteAktivitaet="datetime('now','localtime')")
        self.__AktualisiereButtonNutzerAktivitaet(self.__LabelKontoBestellung_NutzerName.get_label())
        # Log-Nachricht vorbereiten
        LogNachricht = "{} € aufgeladen durch {}".format(self.__LabelKontoAufladen_Gesamtbetrag.get_label(), self.__LabelKontoBestellung_NutzerName.get_label())
        self.__Datenbank.SchreibeNeueZeilen("Log", "zeitpunkt, nachricht", zeitpunkt="datetime('now','localtime')", nachricht=LogNachricht)
        # Anzeigen anpassen bzw. zuruecksetzen.
        if self.__SpuelEingeloest:
            self.__ZeitpunktSpuelEingeloest = datetime.today()
            self.__SpuelEingeloest = False
        self.__AktualisiereLabelKontostand()
        # Abschliessen der GUI-Anzeige
        self.__WindowKontoAufladen.hide()
        self.__WindowKontoBestellung.show_all()

    def __ResetWindowKontoAufladen(self):
        # Alle Buttons und interne Variablen werden zurueckgesetzt
        self.__LabelKontoAufladen_Gesamtbetrag.set_label("0")
        self.__ButtonKontoAufladen_Bestaetigen.set_sensitive(False)
        self.__ButtonKontoAufladen_Korrektur.set_sensitive(False)
        # Nach festgelegter Zeit wird der ButtonKontoAufladen_BetragIDSpuel wieder freigegeben
        if KKT_Verwaltung.ZeitspanneStunden(self.__ZeitpunktSpuelEingeloest, datetime.today()) > KKT_Parameter.GUI_F1_SpuelFreigabezeit:
            self.__ButtonKontoAufladen_BetragIDSpuel.set_sensitive(True)
        else:
            self.__ButtonKontoAufladen_BetragIDSpuel.set_sensitive(False)
        self.__SpuelEingeloest = False

    # -------------------------- WindowKontoauszug
    # -------------------------------------------
    def AnzeigeWindowKontoauszug(self, GUIButton):
        # Wenn der Bediener auf den ButtonKontoBestellung_Kontoauszug oder ButtonKontoAufladen_Kontoauszug drueckt, wird diese Methode aufgerufen.
        # Es aendert sich die Anzeige innerhalb des ButtonKontoBestellung oder WindowKontoAufladen
        BestellungenGesamt = self.__Datenbank.LeseSpezielleZeilen("Bestellung", 'name="{}"'.format(self.__LabelKontoBestellung_NutzerName.get_label()))
        BestellungenZeitspanne = KKT_Verwaltung.ListeBestellungen(BestellungenGesamt, KKT_Parameter.GUI_F1_KontoauszugTage)
        BestellungenText = ""
        KostenGesamt = 0
        KostenDatenpunkte = [0]
        TagIter = datetime.today().date() - timedelta(days=KKT_Parameter.GUI_F1_KontoauszugTage - 1)
        # Datenreihe der Kosten pro Tag anlegen
        for Bestellung in BestellungenZeitspanne:
            KostenProdukt = self.__Datenbank.LeseSpezielleZeilen("Bestand", 'produkt="{}"'.format(Bestellung[1]))
            try:
                KostenProdukt = KostenProdukt[0][5]
            # Falls das Produkt nicht mehr in der Datenbank gefunden wird
            except IndexError:
                KostenProdukt = 0.0
            KostenGesamt += KostenProdukt
            BestellungTag = Bestellung[0][:Bestellung[0].find(' ')]
            BestellungenText += " " + KKT_Verwaltung.DatumFormatieren(BestellungTag).strftime('%a') + "~" + BestellungTag[BestellungTag.find('-') + 1:] + \
                                " " + Bestellung[0][Bestellung[0].find(' ') + 1:Bestellung[0].rfind(':')] + " --- " + Bestellung[1] + \
                                " - (" + str(KostenProdukt) + " €)" + "\n"
            # Datenreihe der Kosten pro Tag fuer den Graphen anlegen
            DiffTage = KKT_Verwaltung.ZeitspanneTage(BestellungTag, TagIter)
            if DiffTage.days > 1:
                for Tage in range(DiffTage.days - 1):
                    KostenDatenpunkte.append(0)
                KostenDatenpunkte.append(KostenProdukt)
                TagIter += DiffTage
            elif DiffTage.days > 0:
                KostenDatenpunkte.append(KostenProdukt)
                TagIter += DiffTage
            else:
                KostenDatenpunkte[-1] += KostenProdukt
        DiffTageZuHeute = KKT_Verwaltung.ZeitspanneTage(TagIter, datetime.today().date())
        if DiffTageZuHeute.days > 0:
            for Tage in range(DiffTageZuHeute.days):
                KostenDatenpunkte.append(0)
        # Textausgabe erstellen
        self.__LabelKontoauszug_Datum.set_label("{}:  {}".format("Heute", datetime.today().date().strftime('%A %d %b %Y')))
        self.__LabelKontoauszug_Umsatz.set_label("{}".format(str(round(KostenGesamt, 3))))
        self.__TextViewKontoauszug_Liste.set_text(BestellungenText)
        # Datenreihe der "Tage" an die Datenreihe der "Kosten" anpassen - fuer den Ausgaben-Graphen
        TageDatenpunkte = [KKT_Parameter.GUI_F1_KontoauszugTage - 1]
        for Tage in range(len(KostenDatenpunkte) - 1):
            TageDatenpunkte.append(TageDatenpunkte[-1] - 1)
        # Zeichnen des Ausgaben-Graphen
        Graph = Figure()
        Graph.subplots_adjust(left=0.13, bottom=0.18, right=0.97, top=0.94)
        GraphIntern = Graph.add_subplot(111)
        GraphIntern.set_xlabel('Tage in die Vergangenheit')
        GraphIntern.set_ylabel('Ausgaben pro Tag in €')
        YAchsMin = 0        # Skalierung der Y-Achse in Euro
        YAchsMax = 13       # Skalierung der Y-Achse in Euro
        GraphIntern.set_yticks(np.arange(YAchsMin, YAchsMax, 1))
        XAchsStep = int(KKT_Parameter.GUI_F1_KontoauszugTage / 15)
        GraphIntern.set_xticks(np.arange(0, KKT_Parameter.GUI_F1_KontoauszugTage + XAchsStep, XAchsStep))
        GraphIntern.set_xlim(0, KKT_Parameter.GUI_F1_KontoauszugTage)    # Damit wird die X-Achsenskalierung fixiert, sodass diese immer gleich ist
        GraphIntern.set_ylim(YAchsMin-0.1, YAchsMax-0.8)                 # Damit wird die Y-Achsenskalierung fixiert, sodass diese immer gleich ist
        GraphIntern.grid(axis='both', linestyle='--', linewidth=0.5)
        GraphIntern.step(TageDatenpunkte, KostenDatenpunkte, where='mid')
        GraphIntern.fill_between(TageDatenpunkte, KostenDatenpunkte, step='mid')
        # Den aktuellen Wochentag (oben als Text) zum Ausgaben-Graphen hinzufuegen
        GraphIntern.annotate(datetime.today().date().strftime('%a'),
                             xy=(0, YAchsMax-1.3),
                             xytext=(0, 5),  # 5 points vertical offset.
                             textcoords='offset points',
                             ha='center', va='bottom')
        # Die Sonntage zum Ausgaben-Graphen (oben als Text) hinzufuegen
        if datetime.today().date().isoweekday() != 7:
            SonntageDatenpunkte = np.arange(datetime.today().date().isoweekday(), KKT_Parameter.GUI_F1_KontoauszugTage, 7)
        else:
            SonntageDatenpunkte = np.arange(0, KKT_Parameter.GUI_F1_KontoauszugTage, 7)
        for Sonntag in SonntageDatenpunkte:
            if Sonntag <= 1: continue    # Sieht sonst in dem Graphen nicht schoen aus (Schrift ueberlappt sich)
            if Sonntag == 2 and KKT_Parameter.GUI_F1_KontoauszugTage > 30: continue
            GraphIntern.annotate("So",
                        xy=(Sonntag, YAchsMax-1.3),
                        xytext=(0, 5),  # 5 points vertical offset.
                        textcoords='offset points',
                        ha='center', va='bottom')
        # Sonntage und Samstage (Wochenende) im Ausgaben-Graphen grau markieren
        WochenendeXDatenpunkte = []
        WochenendeYDatenpunkte = []
        for Tag in range(KKT_Parameter.GUI_F1_KontoauszugTage, -1, -1):
            WochenendeXDatenpunkte.append(Tag)
            if Tag in SonntageDatenpunkte or Tag - 1 in SonntageDatenpunkte:  # Sonntage und Samstage hinzufuegen
                WochenendeYDatenpunkte.append(YAchsMax+2)
            else:
                WochenendeYDatenpunkte.append(YAchsMin-2)
        if datetime.today().date().isoweekday() == 6:   # Falls heute Samstag ist
            WochenendeYDatenpunkte[-1] = YAchsMax + 2
        GraphIntern.fill_between(WochenendeXDatenpunkte, WochenendeYDatenpunkte, YAchsMin-4, step='mid', alpha=0.2, color='#7F7F7F')
        # Einbinden des Ausgaben-Graphen in PyGTK
        if len(self.__ScrolledwindowKontoauszug.get_children()) > 0:  # Sonst kann der Graph nicht neu gezeichnet werden
            self.__ScrolledwindowKontoauszug.get_children()[0].destroy()
        self.__ScrolledwindowKontoauszug.add(FigureCanvas(Graph))
        # Abschliessen der GUI-Anzeige
        self.__WindowKontoBestellung.hide()
        self.__WindowKontoAufladen.hide()
        self.__WindowKontoauszug.show_all()

    def on_ButtonZurueckKontoauszug_clicked(self, GUIButton):
        # Wenn der Bediener auf den ButtonKontoauszug_Zurueck drueckt, wird diese Methode aufgerufen.
        # Damit geht die Anzeige wieder zurueck zum WindowKontoBestellung
        self.__WindowKontoauszug.hide()
        self.__WindowKontoBestellung.show_all()

    # ------------------------- WindowBestandAendern
    # ---------------------------------------------
    def __AnzeigeWindowBestandAendern(self, GUIObjekt, Produkt):
        # Wenn der Bediener den Button eines Produktes fuer die festgelegte Zeitspanne drueckt, wird ein neues Fenster geoeffnet.
        # Siehe Zeitspanne GUI_F2_ButtonProduktPressedZeitspanne
        self.__LabelBestandAendern_Produkt.set_label(Produkt)
        BestandAlt = self.__Datenbank.LeseSpezielleZeilen("Bestand", 'produkt="{}"'.format(Produkt))[0][2]
        self.__LabelBestandAendern_Bestand.set_label(str(BestandAlt))
        self.__ButtonBestandAendern_Erhoehen.set_active(True)
        self.__SpinbuttonBestandAendern_Reduzieren.set_sensitive(False)
        self.__ButtonBestandAendern_Diebstahl.set_sensitive(False)
        self.__SpinbuttonBestandAendern_Erhoehen.set_value(50)
        self.__SpinbuttonBestandAendern_Reduzieren.set_value(0)
        self.__AdjustmentBestandAendern_Reduzieren.set_upper(BestandAlt)
        self.__AdjustmentBestandAendern_Erhoehen.set_lower(-BestandAlt)
        # Abschliessen der GUI-Anzeige
        self.__WindowBestandAendern.show_all()
        self.__WindowBestandAendern.present()
        # Bestandsaenderungen und Aenderungen an WindowKontoBestellung muessen rueckgaengig gemacht werden
        self.__ResetWindowKontoBestellung()

    def on_ButtonKategorieBestandAendern_clicked(self, GUIButton):
        # Wenn der Bediener den ButtonKategorieBestandAendern drueckt, wird diese Methode aufgerufen.
        if GUIButton.get_active():
            if GUIButton.get_name() == "IDUp":
                self.__SpinbuttonBestandAendern_Erhoehen.set_sensitive(True)
                self.__SpinbuttonBestandAendern_Reduzieren.set_sensitive(False)
                self.__ButtonBestandAendern_Diebstahl.set_sensitive(False)
                self.__ButtonBestandAendern_Bestaetigen.set_sensitive(True)
                self.__SpinbuttonBestandAendern_Reduzieren.set_value(0)
            if GUIButton.get_name() == "IDDown":
                self.__SpinbuttonBestandAendern_Erhoehen.set_sensitive(False)
                self.__SpinbuttonBestandAendern_Reduzieren.set_sensitive(True)
                self.__ButtonBestandAendern_Diebstahl.set_sensitive(True)
                self.__ButtonBestandAendern_Bestaetigen.set_sensitive(False)
                self.__SpinbuttonBestandAendern_Erhoehen.set_value(50)

    def on_ButtonDiebstahl_clicked(self, GUIButton):
        # Wenn der Bediener den ButtonBestandAendern_Diebstahl drueckt, wird diese Methode aufgerufen.
        # Der Bestand wird auf den gewuenschten Wert gesetzt, in die Datenbank geschrieben und die Differenz dem Diebstahlkonto angerechnet
        BestandAlt = self.__Datenbank.LeseSpezielleZeilen("Bestand", 'produkt="{}"'.format(self.__LabelBestandAendern_Produkt.get_label()))[0][2]
        BestandNeu = self.__SpinbuttonBestandAendern_Reduzieren.get_value_as_int()
        if BestandAlt == BestandNeu:
            pass
        else:
            self.__Datenbank.UeberschreibeZeile("Bestand", 'produkt="{}"'.format(self.__LabelBestandAendern_Produkt.get_label()), anzahl=BestandNeu)
            # Die Differenz im Bestand wird dem Diebstahlkonto angerechnet
            KostenGesamt = 0
            KostenProdukt = self.__Datenbank.LeseSpezielleZeilen("Bestand", 'produkt="{}"'.format(self.__LabelBestandAendern_Produkt.get_label()))[0][5]
            for Bestand in range(BestandNeu, BestandAlt):
                KostenGesamt += KostenProdukt
                self.__Datenbank.SchreibeNeueZeilen("Bestellung", "zeitpunkt, produkt, name", zeitpunkt="datetime('now','localtime')",
                                                    produkt=self.__LabelBestandAendern_Produkt.get_label(), name="Diebstahlkonto")
            # Nun wird der Kontostand des Diebstahlkontos angepasst und in die Datenbank geschrieben
            KontostandNeu = round(self.__Datenbank.LeseSpezielleZeilen("Nutzer", 'name="{}"'.format("Diebstahlkonto"))[0][2] - KostenGesamt, 3)
            self.__Datenbank.UeberschreibeZeile("Nutzer", 'name="{}"'.format("Diebstahlkonto"), kontostand=KontostandNeu)
            # Log-Nachricht vorbereiten
            LogNachricht = "Bestand von '{}' wurde von {} auf {} gesetzt. Nicht abgerechnete Produkte: {}".format(self.__LabelBestandAendern_Produkt.get_label(),
                                                                                                                  BestandAlt, BestandNeu, BestandAlt - BestandNeu)
            self.__Datenbank.SchreibeNeueZeilen("Log", "zeitpunkt, nachricht", zeitpunkt="datetime('now','localtime')", nachricht=LogNachricht)
        # Abschliessen der GUI-Anzeige
        self.__LabelBestandAendern_Bestand.set_label(str(BestandNeu))
        self.__ButtonBestandAendern_Erhoehen.set_active(True)
        self.__AdjustmentBestandAendern_Reduzieren.set_upper(BestandNeu)
        self.__AdjustmentBestandAendern_Erhoehen.set_lower(-BestandNeu)
        # Neuen Bestand im Hintergrund fuer WindowKontoBestellung aendern
        self.__ResetWindowKontoBestellung()

    def on_ButtonBestaetigenBestandAendern_clicked(self, GUIButton):
        # Wenn der Bediener den ButtonBestaetigenBestandAendern drueckt, wird diese Methode aufgerufen.
        # Der neue Bestand wird in die Datenbank geschrieben
        BestandAlt = self.__Datenbank.LeseSpezielleZeilen("Bestand", 'produkt="{}"'.format(self.__LabelBestandAendern_Produkt.get_label()))[0][2]
        BestandNeu = BestandAlt + self.__SpinbuttonBestandAendern_Erhoehen.get_value_as_int()
        if BestandNeu >= 0:
            self.__Datenbank.UeberschreibeZeile("Bestand", 'produkt="{}"'.format(self.__LabelBestandAendern_Produkt.get_label()), anzahl=BestandNeu)
            # Log-Nachricht vorbereiten
            LogNachricht = "Bestand von '{}' wurde von {} auf {} gesetzt. Um {} Produkte geaendert".format(self.__LabelBestandAendern_Produkt.get_label(),
                                                                                                           BestandAlt, BestandNeu,
                                                                                                           self.__SpinbuttonBestandAendern_Erhoehen.get_value_as_int())
            self.__Datenbank.SchreibeNeueZeilen("Log", "zeitpunkt, nachricht", zeitpunkt="datetime('now','localtime')", nachricht=LogNachricht)
        # Abschliessen der GUI-Anzeige
        self.__WindowBestandAendern.hide()
        # Neuen Bestand im Hintergrund fuer WindowKontoBestellung aendern
        self.__ResetWindowKontoBestellung()

    def __ResetWindowKontoBestellung(self):
        # Bestandsaenderungen und Aenderungen an WindowKontoBestellung muessen rueckgaengig gemacht werden
        # Da beim Druecken des Buttons fuer ein Produkt auch "on_ButtonProdukt_clicked" aufgerufen wird, muessen Aenderungen rueckgaengig gemacht werden
        self.__Bestellung.clear()
        self.__BestellungKosten = 0
        self.__LabelKontoBestellung_Produktanzahl.set_label("0")
        for Button in self.__ButtonsProdukt:
            Bestand = self.__Datenbank.LeseSpezielleZeilen("Bestand", 'produkt="{}"'.format(Button.LeseID()))[0][2]
            Button.AnpassenLabelUnterButton(Bestand)
            self.__ProduktBestand[Button.LeseID()][0] = Bestand
            self.__ProduktBestand[Button.LeseID()][1] = Bestand
        self.__ButtonKontoBestellung_Kaufen.set_sensitive(False)
        self.__ButtonKontoBestellung_Korrektur.set_sensitive(False)
        self.__ButtonKontoBestellung_DrTitel.set_sensitive(True)

    def __delete_event_BestandAendern(self, GUIObjekt, Event):
        # Wenn der Bediener durch "X" das Fenster schliesst, wird diese Methode aufgerufen.
        GUIObjekt.hide()
        return True  # Das muss laut Wiki gemacht werden

    # ------------------------------------ Kleinere Funktionen
    # -------------------------------------------------------
    def __AktualisiereButtonNutzer(self, NutzerNameAlt, NutzerNameNeu):
        # Hiermit kann der Name eines Nutzers auf dem Button und auch in der Datenbank aktualisiert werden.
        # Stellt sicher, dass es zu keinen Widerspruechen kommt.
        for Button in self.__ButtonsNutzer:
            if Button.LeseID() == NutzerNameAlt:
                Button.SchreibeID(NutzerNameNeu)
                # Aktualisiere NutzerNamen in Datenbank
                self.__Datenbank.UeberschreibeZeile("Nutzer", 'name="{}"'.format(NutzerNameAlt), name=NutzerNameNeu)
                self.__AktualisiereButtonNutzerAktivitaet(NutzerNameNeu)
                break

    def __AktualisiereButtonNutzerAktivitaet(self, NutzerName):
        # Hiermit wird die Anzeige der letzten Aktivitaet auf dem Button des Nutzers aktualisiert.
        # Entweder wird ein Datum der letzten Aktivitaet hinzugefuegt oder es wird entfernt.
        for Button in self.__ButtonsNutzer:
            if Button.LeseID() == NutzerName:
                NutzerAktivitaet = self.__Datenbank.LeseSpezielleZeilen("Nutzer", 'name="{}"'.format(NutzerName))[0][5]
                NutzerAktivitaetDatumFormatiert = NutzerAktivitaet[:NutzerAktivitaet.find(' ')]
                if not KKT_Verwaltung.ZeitspanneCheckMaxZeitspanne(NutzerAktivitaetDatumFormatiert, KKT_Parameter.GUI_F1_NutzerInaktivTage):
                    Button.get_child().set_markup("<b>{}</b><span color='#4F5F99'><b>{}</b></span>".format(self.__FormatiereNutzerName(NutzerName),
                                                                                                           "\n" + NutzerAktivitaetDatumFormatiert))
                else:
                    Button.get_child().set_markup("<b>{}</b>".format(self.__FormatiereNutzerName(NutzerName)))

    def __AktualisiereLabelKontostand(self):
        # Hiermit wird der Kontostand angezeigt bzw. aktualisiert und gegebenenfalls rot markiert
        Kontostand = self.__Datenbank.LeseSpezielleZeilen("Nutzer", 'name="{}"'.format(self.__LabelKontoBestellung_NutzerName.get_label()))[0][2]
        if Kontostand <= KKT_Parameter.GUI_F1_MaxSchulden/3:
            self.__LabelKontoBestellung_Kontostand.set_markup("<span color='red'>{} €</span>".format(Kontostand))
            self.__LabelKontoAufladen_Kontostand.set_markup("<span color='red'>{} €</span>".format(Kontostand))
            self.__LabelKontoauszug_Kontostand.set_markup("<span color='red'>{} €</span>".format(Kontostand))
        else:
            self.__LabelKontoBestellung_Kontostand.set_label("{} €".format(Kontostand))
            self.__LabelKontoAufladen_Kontostand.set_label("{} €".format(Kontostand))
            self.__LabelKontoauszug_Kontostand.set_label("{} €".format(Kontostand))

    def __LeseNutzerNamenAusDatenbank(self):
        # Hier werden die Nutzer aus der Datenbank gelesen und in die drei Kategorien einsortiert.
        NutzerNamenSortiert = [[], [], []]  # Sortiert nach Kategorie (z. B. Permanente, wissenschaftliche Mitarbeiter und Studierende) und nach Eintrittszeit
        NutzerGesamt = self.__Datenbank.LeseAlleZeilen("Nutzer")
        for Nutzer in NutzerGesamt:
            if Nutzer[1] == "Diebstahlkonto":  # Auf dieses Konto koennen alle nicht bezahlten Produkte gebucht werden. Es erscheint nicht in der Uebersicht
                continue
            elif Nutzer[3] == 0:
                NutzerNamenSortiert[0].append(Nutzer[1])
            elif Nutzer[3] == 1:
                NutzerNamenSortiert[1].append(Nutzer[1])
            elif Nutzer[3] == 2:
                NutzerNamenSortiert[2].append(Nutzer[1])
        return NutzerNamenSortiert

    def __FormatiereNutzerName(self, NutzerName):
        # Hier werden bei Bedarf Zeilenumbrueche eingefuegt, damit die Labels von ButtonNutzer nicht zu lange werden
        # ab 15 Zeichen muss es einen Zeilenumbruch im Label geben
        def ZweiterZeilenumbruch(FormatierterNutzerName):
            KlammerIndex = NutzerName.rfind("[")
            if KlammerIndex != -1:  # Es existiert ein Betreuer fuer den Nutzer
                return FormatierterNutzerName[:KlammerIndex] + "\n" + FormatierterNutzerName[KlammerIndex:]
            else:
                DrIndex2 = NutzerName.rfind("Dr.")
                if DrIndex2 != -1:
                    return FormatierterNutzerName[:DrIndex2 + 4 + 13] + "--\n" + FormatierterNutzerName[DrIndex2 + 4 + 13:]
                else:
                    return FormatierterNutzerName[:13] + "--\n" + FormatierterNutzerName[13:]
        DrIndex = NutzerName.rfind("Dr.")
        if DrIndex != -1:
            if NutzerName.find("Dr. mult.") != -1:
                NutzerName = NutzerName[:DrIndex + 10] + "\n" + NutzerName[DrIndex + 10:]
            else:
                NutzerName = NutzerName[:DrIndex + 4] + "\n" + NutzerName[DrIndex + 4:]
        if NutzerName.rfind("\n") != -1:  # Es wurde schon ein Zeilenumbruch fuer die Titel hinzugefuegt
            if (len(NutzerName) - NutzerName.rfind("\n") - 1) > 14:
                return ZweiterZeilenumbruch(NutzerName)
            else:
                return NutzerName
        else:  # Es wurde noch kein Zeilenumbruch fuer die Titel hinzugefuegt
            if len(NutzerName) > 14:
                return ZweiterZeilenumbruch(NutzerName)
            else:
                return NutzerName

    def __FormatiereNutzerNameDrTitel(self, NutzerName):
        # Diese Methode ermittelt, wie viele Doktortitel bisher in dem Namen auftauchen und passt gegebenfalls den Namen an
        # Diese Methode darf nur aufgerufen werden, wenn ein Doktortitel gekauft wurde, da in jedem Fall ein Titel dem Namen hinzugefuegt wird
        if NutzerName.find("Dr. mult. ") != -1:
            return NutzerName
        DrIndex = NutzerName.find("Dr.")
        DrAnzahl = 0
        while True:
            if DrIndex < 0:
                break
            else:
                DrAnzahl += 1
                DrIndex = NutzerName.find("Dr.", DrIndex + 1)
        if DrAnzahl > 1:
            if NutzerName.find("Prof.") != -1:
                return "Prof. Dr. mult. " + NutzerName[NutzerName.rfind("Dr.") + 4:]
            else:
                return "Dr. mult. " + NutzerName[DrAnzahl * 4:]
        else:
            if NutzerName.find("Prof.") != -1:
                return NutzerName[:NutzerName.rfind("Dr.") + 4] + "Dr. " + NutzerName[NutzerName.rfind("Dr.") + 4:]
            else:
                return "Dr. " + NutzerName

    def __VereinheitlicheNutzerName(self, NutzerName):
        # Vereinheitlicht den Namen des Nutzers, sodass alle Namen in der Datenbank aehnlich aufgebaut sind.
        NutzerName = NutzerName.lstrip()  # Leerzeichen am Anfang entfernen
        NutzerName = NutzerName.rstrip()  # Leerzeichen am Ende entfernen
        PunktIndex = NutzerName.rfind(".")
        LeerzeichenIndex = NutzerName.find(" ")
        if LeerzeichenIndex == -1:
            if PunktIndex == -1:
                NutzerName = NutzerName[:1].upper() + NutzerName[1:].lower()
            else:
                NutzerName = NutzerName[:PunktIndex + 1].upper() + " " + NutzerName[PunktIndex + 1:PunktIndex + 2].upper() + NutzerName[PunktIndex + 2:].lower()
        else:
            if PunktIndex != -1 and PunktIndex > LeerzeichenIndex:  # Nachname abgekuerzt?!
                NutzerName = NutzerName[:1].upper() + ". " + NutzerName[LeerzeichenIndex + 1:]
            else:
                if NutzerName.count(" ") > 1:  # Zwei Vornamen: Zweiter Vorname wird entfernt
                    NutzerName = NutzerName[:LeerzeichenIndex] + NutzerName[NutzerName.rfind(" "):]
                NutzerName = NutzerName[:LeerzeichenIndex + 2].upper() + NutzerName[LeerzeichenIndex + 2:].lower()
                if PunktIndex == -1:
                    NutzerName = NutzerName[:1] + ". " + NutzerName[LeerzeichenIndex + 1:]
        return NutzerName

    # -------------- Threadfunktionen, die immer wieder ausgefuehrt werden
    # -------------------------------------------------------------------
    def __StarteInterneVerwaltung(self):
        try:    # Checken, ob Nutzer schon laenger nicht mehr aktiv waren und falls Ja -> Datum der letzten Aktion auf ButtonNutzer anzeigen!
            self.CheckeLetzteNutzerAktivitaet()
        except:
            self.__ThreadFehlerAnzeige("CheckeLetzteNutzerAktivitaet")
        try:    # Checken, ob es gerade Geburtstagskinder gibt und falls Ja -> Diese anzeigen!
            self.CheckeGeburtstage()
        except:
            self.__ThreadFehlerAnzeige("CheckeGeburtstage")
        try:    # Checken, ob eine Mail geschrieben werden darf und falls Ja -> Aktiv werden!
            self.CheckeMailStatus()
        except:
            self.__ThreadFehlerAnzeige("CheckeMailStatus")
        try:    # Checken, ob eine Woche vergangen ist und und falls Ja -> Speziellen Log schreiben!
            self.CheckeLogStatus()
        except:
            self.__ThreadFehlerAnzeige("CheckeLogStatus")
        return True  # Damit wird der Thread (Timer) nicht beendet wird

    def __ThreadFehlerAnzeige(self, FehlerFunktion):
        if not self.__ThreadFehler:
            self.__ThreadFehler = True    # Damit nicht immer wieder ein Log geschrieben wird
            LogNachricht = "Der Thread 'InterneVerwaltung' wirft einen Fehler bei {}".format(FehlerFunktion)
            self.__Datenbank.SchreibeNeueZeilen("Log", "zeitpunkt, nachricht", zeitpunkt="datetime('now','localtime')", nachricht=LogNachricht)
        if self.__ThreadFehler:
            # Abschliessen der GUI-Anzeige
            self.__ImageNutzer_Status.set_from_icon_name("gtk-no", 4)

    def CheckeLetzteNutzerAktivitaet(self):
        # Checkt, ob bei Nutzern, die schon lange nicht mehr aktiv waren, ein eingefaerbtes "Zuletzt-Aktiv-Datum" hinzugefuegt werden muss.
        for Button in self.__ButtonsNutzer:
            NutzerAktivitaet = self.__Datenbank.LeseSpezielleZeilen("Nutzer", 'name="{}"'.format(Button.LeseID()))[0][5]
            NutzerAktivitaetDatumFormatiert = NutzerAktivitaet[:NutzerAktivitaet.find(' ')]
            if not KKT_Verwaltung.ZeitspanneCheckMaxZeitspanne(NutzerAktivitaetDatumFormatiert, KKT_Parameter.GUI_F1_NutzerInaktivTage):
                Button.get_child().set_markup("<b>{}</b><span color='#4F5F99'><b>{}</b></span>".format(self.__FormatiereNutzerName(Button.LeseID()),
                                                                                                       "\n" + NutzerAktivitaetDatumFormatiert))

    def CheckeGeburtstage(self):
        # Checkt, ob die Anzeige von Geburtstagskindern bevorsteht (wenn die Geburtstage innerhalb der Zeitspanne GUI_F1_GeburtstagTage liegen).
        global Zufallszahl
        self.__LabelNutzer_Geburtstage.set_visible(False)
        self.__LabelNutzer_GeburtstageText.set_visible(False)
        ListeGeburtstage = KKT_Verwaltung.ListeGeburtstageNutzer(self.__Datenbank.LeseAlleZeilen("Nutzer"))
        if len(ListeGeburtstage) > 0:
            self.__LabelNutzer_Geburtstage.set_visible(True)
            self.__LabelNutzer_GeburtstageText.set_visible(True)
            GeburtstageText = ""
            for Geburtstag in ListeGeburtstage:
                GeburtstageText += Geburtstag[0] + ": " + Geburtstag[1] + " | "
            else:
                GeburtstageText = GeburtstageText[:-3]
            if len(GeburtstageText) > 95:
                if Zufallszahl.randint(0, 1) == 0:
                    self.__LabelNutzer_GeburtstageText.set_label(GeburtstageText[:-(len(GeburtstageText) - 95)])
                else:
                    self.__LabelNutzer_GeburtstageText.set_label(GeburtstageText[(len(GeburtstageText) - 95):])
            else:
                self.__LabelNutzer_GeburtstageText.set_label(GeburtstageText)

    def CheckeMailStatus(self):
        # Checkt, ob eine Mail versendet werden darf (je nach Status GUI_F2_MailSchreibenStatus (Ja/Nein) und MailSendenCheck()).
        def SchreibeNachrichtBestand(ProdukteGesamt):
            NachrichtBestand = "Der Bestand von folgenden Produkten ist knapp:\n"
            for Produkt in ProdukteGesamt:
                if int(Produkt[2]) < int(Produkt[4]):
                    NachrichtBestand += "- {}: Soll {} aber IST {}\n".format(Produkt[1], Produkt[4], Produkt[2])
            return NachrichtBestand
        if KKT_Parameter.GUI_F2_MailSchreibenStatus:
            if KKT_Verwaltung.MailSendenCheck() == 0:   # Bedarf einer großen Mail (Logs der letzten Woche und Status zu Bestand)
                # Wenn diese Mail geschrieben werden darf, dann ist eine Woche vergangen
                # Zunaechst die letzten 100 Logs aus der Tabelle "Log" holen (sollten Logs weit ueber eine Woche hinaus sein ...)
                LogMAXPrimaryKey = self.__Datenbank.LeseSpezielleZeilen("Log", 'primary_key=(SELECT MAX(primary_key) FROM Log)')[0][0]
                LogsGesamt = self.__Datenbank.LeseSpezielleZeilen("Log", 'primary_key>{}'.format(LogMAXPrimaryKey - 100))
                # Nun wird ueberprueft, welche Logs aus der letzten Woche stammen
                NachrichtGesamt = "Logs aus der letzten Woche:\n"
                for Log in LogsGesamt:
                    if KKT_Verwaltung.ZeitspanneCheckDatum(Log[1]):
                        NachrichtGesamt += "- " + Log[2] + "({})\n".format(Log[1][:10])
                else:
                    NachrichtGesamt += "\n"
                if self.__UmsatzWoche > 0:
                    NachrichtGesamt += "Der Wochenumsatz lag in der letzten Woche bei {} €\n\n".format(self.__UmsatzWoche)
                NachrichtGesamt += SchreibeNachrichtBestand(self.__Datenbank.LeseAlleZeilen("Bestand"))
                KKT_Verwaltung.MailSenden(NachrichtGesamt)
            elif KKT_Verwaltung.MailSendenCheck() == 1:     # Bedarf einer kleinen Mail (nur Status zu Bestand).
                KKT_Verwaltung.MailSenden(SchreibeNachrichtBestand(self.__Datenbank.LeseAlleZeilen("Bestand")))

    def CheckeLogStatus(self):
        # Checkt, ob eine Woche vergangen ist und schreibt nach dieser Zeitspanne spezielle Logs (z. B. Umsatz der letzten Woche).
        DiffTageZuHeute = KKT_Verwaltung.ZeitspanneTage(self.__ZeitpunktLogStatus, datetime.today().date())
        if DiffTageZuHeute.days >= 7:
            LogNachricht = "Der Wochenumsatz lag in der letzten Kalenderwoche (KW{}) bei {} €".format(datetime.today().isocalendar()[1] - 1, self.__UmsatzWoche)
            self.__Datenbank.SchreibeNeueZeilen("Log", "zeitpunkt, nachricht", zeitpunkt="datetime('now','localtime')", nachricht=LogNachricht)
            self.__UmsatzWoche = 0
            self.__ZeitpunktLogStatus = datetime.today().date()


if __name__ == "__main__":
    MainWindowKKT = MainWindow()
    MainWindowKKT.StartenGUIKKT()
