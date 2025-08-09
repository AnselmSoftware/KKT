<div align="center"> 
   
# KKT

### ☕️ Software für die digitale Kaffeeküche komplett in Python geschrieben. ☕️


Deutsch | English

**A detailed readme in English will follow soon ...**

</div>

## Übersicht
KKT (Kaffeekassentool) ist eine Software mit grafischer Benutzeroberfläche, die es vielen Nutzern einer Kaffeeküche ermöglicht, selbstständig Produkte wie beispielsweise Kaffee abzurechnen. Dies erleichtert die Verwaltung der Kaffeeküche bzw. Kaffeekasse und gibt jedem Nutzer einen Überblick über seine Ausgaben und Einzahlungen.

Wesentliche Merkmale:
- **Digital** – Es gibt keine nervigen Kaffeelisten mehr, aus denen die Ausgaben der Nutzer händisch ermittelt werden müssen.
- **Benutzerfreundlich**  – Schlanke Übersicht aller Nutzer durch schlichte Buttons und selbsterklärender Kaufprozess von Produkten.
- **Sicher** – Verwendung einer SQL-Datenbank für alle Daten des KKT bzw. der Nutzer. Diese ermöglicht auch ohne die Software das Auslesen und Sichern der Daten.
- **Einfach zu verwalten** – Vom Anlegen neuer Nutzer und dem Aufladen von Guthaben auf ein Nutzerkonto bis zum Ein- und Austragen vorhandener Produkte ist alles innerhalb der Software möglich, ohne dass eine manuelle Interaktion mit der Datenbank erforderlich ist.
- **Online** – Profitiere als Verantwortlicher vom automatischen Versenden von Statusmails zu Produkten und Ereignissen im KKT.

<div align="center">
    
**-- Foto von RPi + Touchscreen mit laufendem KKT (IAM-WK) --**
</div>

## Funktionen des KKT
Nach dem Start der Software wird eine Übersichtsseite mit allen aktiven Nutzern angezeigt. Diese Übersichtsseite kann als Hauptfenster betrachtet werden. Am unteren Rand der Übersichtsseite befindet sich eine Leiste mit einem grünen Knopf (siehe Abbildung unten). Bei einem internen Fehler in der Software springt dieser Knopf auf Rot. Über diesen Knopf kann ein Fenster geöffnet werden, das Informationen zur Software und deren Entwicklung bereitstellt. In dieser Leiste wird außerdem ein anstehender Geburtstag eines Nutzers angezeigt. Rechts in der Leiste befindet sich ein Button zum Anlegen eines neuen Nutzers.

<div align="center">
    
**-- Screenshot der Übersichtsseite des KKT --**
</div>

Auf der Übersichtsseite werden die Nutzer in drei Gruppen eingeteilt. Diese Gruppen sind in der Software voreingestellt und heißen Permanente, wissenschaftliche Mitarbeiter und Studierende. Andere Gruppennamen können bei Bedarf vergeben werden, indem der Code in KKT_Main.py angepasst wird.
Neue Nutzer werden in einem separaten Fenster angelegt (siehe Abbildung unten). In diesem muss der Name des neuen Nutzers angegeben werden. Dieser muss sinnvoll gewählt werden und wird vor der Anlage des Nutzers überprüft. Des Weiteren wird der Name nach dem Anlegen des Nutzers formatiert. Falls vorhanden, wird der Vorname mit einem Punkt abgekürzt und folgt dem Nachnamen. Zudem muss eine Zuordnung zu einer Gruppe erfolgen. Nutzer der letzten Gruppe (Studierende) müssen einen Betreuer angeben, sodass im Falle eines Ausscheidens des Nutzers eine Person für eventuell verbliebene Schulden geradestehen kann. Der Geburtstag kann angegeben werden (freiwillig), wenn dieser auf der Übersichtsseite erscheinen soll.

<div align="center">
    
**-- Screenshot der Seite Nutzer Anlegen des KKT --**
</div>

Auf der Übersichtsseite können aktive Nutzer durch einen langen Klick gelöscht werden. Hierzu mindestens drei Sekunden lang den Button des jeweiligen Nutzers gedrückt halten (die Zeitspanne kann in KKT_Parameter.py verändert werden). Falls mit dem Nutzer eine Abrechnung des Guthabens/der Schulden stattgefunden hat, kann dies beim Löschen angegeben werden. Gelöschte Nutzer werden automatisch in einer eigenen Tabelle innerhalb der Datenbank archiviert und können so später reaktiviert werden.
Durch einen einfachen Klick auf einen Nutzer wird die Bestellübersicht geöffnet. Oben links wird der Name des Nutzers angezeigt und es wird die Möglichkeit geboten, einen Doktortitel zu erwerben (Spaß-Feature). Zudem wird der aktuelle Kontostand angezeigt und es gibt zwei Buttons, um die letzten Käufe anzuzeigen (Kontoauszug) und das Konto aufzuladen.

<div align="center">
    
**-- Screenshot der Seite Bestellübersicht des KKT --**
</div>

Im Fenster der Bestellübersicht können Produkte für den Kauf ausgewählt werden.

<div align="center">
    
**… weitere Beschreibung folgt noch ...**
</div>

## Installation (auf Raspberry Pi)
Wenn KKT auf einem Raspberry Pi mit Touchscreen installiert werden soll, muss dieser zunächst vollständig mit einer Desktopumgebung eingerichtet werden. KKT benötigt verschiedene Pakete bzw. Python-Bibliotheken, die installiert sein müssen:
- **GTK 3.0** – In der Regel in Raspbian / Raspberry Pi OS enthalten.
- **Python3.x** – In der Regel in Raspbian / Raspberry Pi OS enthalten.
- **python3-gi-cairo** – Für die Darstellung der Diagramme innerhalb der Software.
```
sudo apt-get install python3-gi-cairo
```
- **python3-numpy** – Für die Erstellung der Diagramme innerhalb der Software.
```
sudo apt-get install python3-numpy
```
- **python3-matplotlib** – Ebenfalls für die Erstellung der Diagramme innerhalb der Software.
```
sudo apt-get install python3-matplotlib
```
- **unclutter** (optional) – Lässt den Mauszeiger verschwinden. Allerdings funktioniert das mit dem neuen Raspberry Pi OS nicht mehr (Grund hierfür ist der Wechsel auf Wayland).
```
sudo apt-get install unclutter
```
- **xscreensaver** (optional) – Vermeidet einen Sperrbildschirm, der bei Berührung im Hintergrund einen Klick ausführt (https://stackoverflow.com/questions/30985964/how-to-disable-sleeping-on-raspberry-pi). Funktioniert unter Umständen mit dem neuen Raspberry Pi OS nicht mehr.
```
sudo apt-get install xscreensaver
```

Es kann außerdem praktisch sein, einen Server so einzurichten, dass ein Ordner auf dem Gerät (Raspberry Pi) als Netzwerklaufwerk auf einem anderen Gerät eingebunden werden kann, um (automatische) Backups der Datenbank durchzuführen. Hierfür kann beispielsweise ein Samba-Server eingesetzt werden. In diesem Fall ist von der SQL-Datenbank `KKT_database.sqlite` ein regelmäßiges Backup anzulegen.

KKT kann entweder über die Konsole im Ordner der Software mit dem Befehl
```
sudo python3.x KKT_Main.py
```
gestartet werden, wobei `x` für die installierte Python-Version steht. Alternativ kann ein einfaches Bash-Skript auf dem Desktop platziert werden, das durch einen Klick die Software startet. Beispielhafter Code für das Bash-Skript:
```
!/bin/bash
cd Ordner
sudo python3.x ./KKT_Main.py
```
Die Bezeichnung `Ordner` ist hierbei durch den Namen des selbst angelegten Ordners zu ersetzen.
Wichtig: Das KKT muss innerhalb einer laufenden grafischen Benutzeroberfläche gestartet werden.

Sollte das KKT zu diesem Zeitpunkt noch nicht starten, könnte das an fehlenden Paketen liegen. Die noch fehlenden Pakete werden in diesem Fall anhand der Fehlermeldungen identifiziert und installiert.

## Aufbau des KKT
Die Software besteht aus den einzelnen Python-Dateien `KKT_Main.py`, `KKT_Parameter.py`, `KKT_Verwaltung.py`, `GUIElemente.py` und `DBVerwaltung.py`. Zudem sind die beiden Dateien `KKT_GUI.glade` und `GUITastatur.glade` enthalten aus denen die grafische Benutzeroberfläche aufgebaut wird. Des Weiteren ist die Datenbank `KKT_database.sqlite` für alle Daten des KKT bzw. der Nutzer enthalten sowie einige Bilder `KKT_img_Warning.png`, `KKT_img_Purchased.png`, `KKT_img_Stop.png`, `KKT_img_Logo.png`, `KKT_img_QRCode.png`, die innerhalb der Software dargestellt werden. Für den Verantwortlichen der Kaffeeküche sind nur die folgenden Dateien von Interesse:
- `KKT_Main.py`
- `KKT_Parameter.py`
- `KKT_database.sqlite`
- `KKT_img_QRCode.png`

Zum Starten der Software muss `KKT_Main.py` aufgerufen werden (siehe Abschnitt oben). `KKT_Parameter.py` und `KKT_img_QRCode.png` müssen angepasst werden (siehe Abschnitt unten) und `KKT_database.sqlite` muss einmalig an die Bedürfnisse der Kaffeeküche bzw. des Verantwortlichen angepasst werden (siehe Abschnitt unten).
Der Code des KKT ist hauptsächlich in der Datei `KKT_Main.py` zu finden. Für Entwickler ist diese Datei die interessanteste erste Anlaufstelle. In der Datei `KKT_Parameter.py` sind alle relevanten Variablen ausgelagert, sodass sie für Änderungen nicht einzeln im Code identifiziert werden müssen. In den übrigen Python-Dateien sind einzelne Funktionen ausgelagert, beispielsweise die Interaktion mit der Datenbank oder die Bereitstellung der Bildschirmtastatur. Die beiden Glade-Dateien `KKT_GUI.glade` und `GUITastatur.glade` wurden mit der Software _Glade 3.40.0_ erstellt und können unter anderem mit dieser Software angepasst werden. In diesen Dateien befinden sich in XML die Informationen vieler GUI-Elemente wie Buttons oder Labels.

## Anpassungen vor Programmstart
Ein besonderes Feature des KKT ist das automatische Versenden von Statusmails. In diesen E-Mails wird der noch vorhandene Bestand von Produkten mitgeteilt, sofern dieser unter einen festgelegten Grenzwert fällt. Zusätzlich werden die letzten Ereignisse des KKT angehängt. Es wird nur eine E-Mail pro Woche mit allen Informationen versendet. E-Mails, die Auskunft über den Bestand geben, können dagegen einmal pro Tag versendet werden.\
Um dieses Feature zu nutzen, muss zunächst ein Mailkonto auf einem Mailserver angelegt werden, auf das per SMTP-Protokoll zugegriffen werden kann. Zudem ist eine stabile Internetverbindung zum Gerät erforderlich, auf dem KKT läuft. In der Datei `KKT_Parameter.py` muss das Feature außerdem eingeschaltet und eingerichtet sein. Da es sich hierbei um ein noch experimentelles Feature handelt, wird bei auftretenden Problemen geraten, das Feature vorerst in der Datei `KKT_Parameter.py` abzuschalten.

Die Datei `KKT_Parameter.py` muss einmalig an die Bedürfnisse der jeweiligen Kaffeeküche bzw. des Verantwortlichen angepasst werden. Die Variablen in der Datei sind in drei Kategorien eingeteilt:  1. Variablen, die die Funktionalität nach außen steuern, 2. Variablen, die die interne/versteckte Funktionalität steuern, 3. Variablen, die nur für Entwickler von Interesse sind. In der Datei sind alle Variablen kommentiert. Folgende Variablen sollten festgelegt werden:
- Maximaler Schuldenstand eines Nutzers
- Gutschrift für das Ausräumen einer Spülmaschine (als Motivation)
- Nach welcher Zeitspanne diese Gutschrift wieder abgerufen werden kann
- Der Preis für den Kauf eines Doktortitels (Spaß-Feature)
- Die Staffelungen der Beträge um die das Konto eines Nutzers aufgeladen werden kann
- Die Bankdaten einer Kaffeeküche bzw. eines Verantwortlichen
- Nach welcher Zeitspanne ein Nutzer als inaktiv markiert wird

Wenn das Feature zum automatischen Versenden von Statusmails genutzt werden soll, muss es aktiviert werden (die Variable muss auf `True` gesetzt werden) und die Informationen zum angelegten Mailkonto müssen in den entsprechenden Variablen gespeichert werden.

Wenn ein Bankkonto für die Kaffeeküche existiert, kann für eine schnelle Überweisung ein QR-Code angelegt werden (siehe eigene Banking-App) und im KKT angezeigt werden. Der QR-Code muss hierfür in der Datei `KKT_img_QRCode.png` gespeichert sein. Die im Beispielbild vorgegebene Auflösung darf hierbei nicht verändert werden!

Die mitgelieferte Datenbank KKT_database.sqlite enthält Beispieldaten in allen zum Programmstart erforderlichen Tabellen und kann sofort in der Software verwendet werden. Es ist allerdings sinnvoll, die Datenbank an die Bedürfnisse der Kaffeeküche bzw. des Verantwortlichen anzupassen. Hierfür kann beispielsweise die Software DB Browser for SQLite verwendet werden.
In der Tabelle Nutzer, die alle aktiven Nutzer des KKT enthält, können die beispielhaften Personen wie Einstein entfernt werden und alle aktiven Nutzer einer Kaffeeküche zum Start hinzugefügt werden. Es ist allerdings auch möglich, aktive Nutzer erst später im KKT anzulegen (siehe oben). Dabei sollte der Nutzer Gästekonto (ein Konto für alle Nutzer) nicht entfernt werden und der Nutzer Diebstahlkonto darf nicht entfernt werden, da die Software sonst nicht ordnungsgemäß funktioniert.
In der Tabelle Bestand müssen die Produkte angelegt werden, die in der Kaffeeküche verkauft werden sollen. Jedes Produkt hat einen Namen, einen Bestand, eine Variable für die Aktivität, einen Sollbestand und einen Preis. Beispielsweise kann das Produkt Kaffee mit einem Bestand von 50 (genug Bohnen für 50 Tassen Kaffee vorhanden), einem Sollbestand von 20 (mindestens 20 Tassen Kaffee sollten immer zur Verfügung stehen), und einem Preis von 0,3 (Einheit Euro) angelegt werden. Die Aktivität ist 0, wodurch das Produkt im KKT angezeigt wird (Produkte mit einer Aktivität von 1 werden nicht angezeigt).

## Aufbau der Datenbank
Die Datenbank besteht aus fünf einzelnen Tabellen, die eine unterschiedliche Anzahl an Variablen enthalten. Die Struktur der Datenbank und die Funktion der Variablen sind in der folgenden Abbildung aufgeschlüsselt:

<img width="1248" height="2950" alt="Übersicht Datenbank" src="https://github.com/user-attachments/assets/4e7ba0b0-14c5-4a0d-b46f-760e37fb94b3" />

Die Tabellen Nutzer und NutzerAlt sind für die Speicherung von Nutzerdaten vorgesehen. Bei der Löschung eines Nutzers werden einige seiner Daten in die Tabelle NutzerAlt transferiert. In der Tabelle Bestand sind die Produkte gespeichert, die im KKT angezeigt und erworben werden können. Eine Anleitung zum Neuanlegen von Produkten finden Sie im Abschnitt „Anpassungen vor Programmstart”. Die Tabellen Bestellung und Log dienen der Auswertung bzw. Kontrolle. In Bestellung werden alle Bestellungen/Käufe von Nutzern protokolliert und in Log sind Systemmeldungen bzw. Ereignisse protokolliert, die auch für eine Fehlersuche oder das Auffinden einer Manipulation herangezogen werden können. Folgende Ereignisse werden protokolliert:
- Neustart der Software
- Anlegen eines neuen Nutzers
- Löschen eines Nutzers (+ Kontostand wurde auf Null gesetzt)
- Kauf eines Doktortitels durch einen Nutzer
- Einzahlung von Geld auf das Konto eines Nutzers
- Änderung des Bestands eines Produkts (+ Angaben zur Art der Änderung)
- Auftreten eines Fehlers im Thread InterneVerwaltung (+ Art des Fehlers)
- Der Wochenumsatz der letzten Kalenderwoche

## Beitragende
Version 1.8 (27. April 2025):\
Komplett designt, programmiert und veröffentlicht von _Anselm Lennard Heuer_

## Lizenz
KKT ist Open-Source und lizenziert unter der GNU General Public License v3.0.
