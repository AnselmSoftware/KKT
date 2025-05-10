"""
Created on 18.12.2019
@author: Anselm Heuer
Version 1.4 - last change on 27.04.2025
Hier werden Methoden zur internen Verwaltung und Verarbeitung von Daten für das Kaffeekassentool bereitgestellt
--Methods for the internal management and processing of data for the coffee tool are provided here--
--Comments in functions are partly written in German - can easily be translated into english with translation programs :)--
"""
# Import all relevant functions and outsourced modules
import KKT_Parameter
from datetime import datetime, timedelta
# Functions and modules for email management
import smtplib
from email.mime.text import MIMEText

# Global parameters for controlling the frequency of mail sending processes
MailGesendetTag = 0
MailGesendetWoche = 0
MailGesendetStatus = False


def ListeBestellungen(Bestellungen, Zeitspanne):
    # Es werden alle Bestellungen aus der uebergebenen Zeitspanne gesammelt und als Liste zurueckgegeben
    ListeBestellungen = []
    for Bestellung in Bestellungen:
        BestellungDatum = Bestellung[1][:Bestellung[1].find(' ')]
        if ZeitspanneCheckMaxZeitspanne(BestellungDatum, Zeitspanne):
            ListeBestellungen.append([Bestellung[1], Bestellung[2]])
    return ListeBestellungen


def ListeGeburtstageNutzer(NutzerGesamt):
    # Es wird bestimmt wer zum aktuellen Zeitpunkt Geburtstag hat. Alle innerhalb eines bestimmten Abstands in Tagen (siehe KKT_Parameter) werden toleriert
    ListeGeburtstageNutzer = []
    for Nutzer in NutzerGesamt:
        if ZeitspanneCheckMaxZeitspanne(Nutzer[4], KKT_Parameter.GUI_F1_GeburtstagTage, ReplaceYear=True):
            ListeGeburtstageNutzer.append([Nutzer[1], Nutzer[4]])
    return ListeGeburtstageNutzer


def ZeitspanneCheckMaxZeitspanne(Datum, MaxZeitspanne, ReplaceYear=False):
    # Die Zeitspanne zwischen dem uebergebenen Datum und dem aktuellen Datum wird bestimmt. Auf Wunsch kann das Jahr ignoriert werden.
    # Dann wird diese berechnete Zeitspanne mit der uebergebenen maximalen Zeitspanne verglichen
    if isinstance(Datum, str):
        if len(Datum) > 0:
            DatumHeute = datetime.today()
            try:
                Datum = datetime.strptime(Datum, '%d.%m.%Y')
            except ValueError:
                Datum = datetime.strptime(Datum, '%Y-%m-%d')
            if ReplaceYear: Datum = Datum.replace(year=DatumHeute.year)
            if abs(DatumHeute - Datum) <= timedelta(days=MaxZeitspanne):
                return True
            else:
                return False
        else: return False
    else: return False


def ZeitspanneCheckDatum(Datum):
    # Ueberprueft, ob das uebergebene Datum in der letzten Kalenderwoche liegt
    Datum = datetime.strptime(Datum, '%Y-%m-%d %X')  # Angepasst an das Format, dass in SQLite fuer ein Datum ausgegeben wird
    if datetime.today().isocalendar()[1] - 1 == Datum.isocalendar()[1]:
        return True
    else: return False


def ZeitspanneStunden(Datum1, Datum2):
    # Es wird die Zeitspanne zwischen dem uebergebenen Datum und dem aktuellen Datum bestimmt und zurueckgegeben (in Stunden)
    Diff = abs(Datum1 - Datum2)
    return Diff.total_seconds() / 60 / 60


def ZeitspanneTage(Datum1, Datum2):
    # Es wird die Zeitspanne zwischen Datum 1 und Datum 2 bestimmt und zurueckgegeben (in Tagen)
    if isinstance(Datum1, str):
        if len(Datum1) > 0:
            try:
                Datum1 = datetime.strptime(Datum1, '%d.%m.%Y').date()
            except ValueError:
                Datum1 = datetime.strptime(Datum1, '%Y-%m-%d').date()
    if isinstance(Datum2, str):
        if len(Datum2) > 0:
            try:
                Datum2 = datetime.strptime(Datum2, '%d.%m.%Y').date()
            except ValueError:
                Datum2 = datetime.strptime(Datum2, '%Y-%m-%d').date()
    return abs(Datum1 - Datum2)


def DatumFormatieren(Datum):
    # Das uebergebene Datum wird formatiert und zurueckgegeben
    if isinstance(Datum, str):
        if len(Datum) > 0:
            try:
                Datum = datetime.strptime(Datum, '%d.%m.%Y').date()
            except ValueError:
                Datum = datetime.strptime(Datum, '%Y-%m-%d').date()
    return Datum


def MailSendenCheck():
    # Es wird bestimmt, ob es dem Programm erlaubt ist, eine Mail zu versenden. Diese Methode soll verhindern, dass immer wieder Mails bei auftretenden Ereignissen
    # versendet werden. Es ist nur eine Mail pro Woche erlaubt. Mails ueber einen niedrigen Bestand duerfen einmal pro Tag gesendet werden.
    global MailGesendetStatus, MailGesendetWoche, MailGesendetTag
    if MailGesendetStatus:
        MailGesendetTag = datetime.today().day
        MailGesendetWoche = datetime.today().isocalendar()[1]
        MailGesendetStatus = False
        return 2  # Mailsenden nicht erlaubt
    if MailGesendetWoche != datetime.today().isocalendar()[1]:
        return 0  # Große Mail darf gesendet werden
    else:
        if MailGesendetTag != datetime.today().day:
            return 1  # Mail, die nur eine Bedarfsmeldung enthaelt, darf gesendet werden
        else:
            return 2  # Mailsenden nicht erlaubt


def MailSenden(Nachricht):
    # Mit dieser Methode werden die Mails versendet. Alle Variablen zum Mailkonto sowie zur Zielmailadresse sind in KKT_Parameter definiert.
    # Aenderungen muessen somit dort vorgenommen werden.
    global MailGesendetStatus
    server = KKT_Parameter.GUI_F2_MailServer
    port = 587  # This is the default Port of an smtp server
    try:
        msg = MIMEText(Nachricht + "\n\nDein Kaffeekassentool", _charset="UTF-8")
        me = KKT_Parameter.GUI_F2_MailAdresse
        you = KKT_Parameter.GUI_F2_MailEmpfaenger
        msg['Subject'] = "Neues aus der Kaffeeküche"
        msg['From'] = me
        msg['To'] = you

        with smtplib.SMTP(host=server, port=port) as smtpObj:
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login(me, KKT_Parameter.GUI_F2_MailPasswort)
            smtpObj.sendmail(me, you, msg.as_string())
            smtpObj.quit()
            MailGesendetStatus = True
    except smtplib.SMTPException:
        print("Error: Problem beim Versenden der E-Mail.")
    except:
        print("Error: Moeglicherweise keine Internetverbindung? Bitte Verbindung pruefen ...")
