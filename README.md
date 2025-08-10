<div align="center"> 
   
# KKT

### ☕️ Software für die digitale Kaffeeküche - komplett in Python geschrieben ☕️

[English](https://github.com/AnselmSoftware/KKT/blob/main/README.md) | [Deutsch](https://github.com/AnselmSoftware/KKT/blob/main/README.md)

</div>

---
> [!NOTE]
> A detailed readme in English will follow soon ..\
> Placeholders will be replaced soon ...
---


## Übersicht
KKT (Kaffeekassentool) ist eine Software mit grafischer Benutzeroberfläche, die es vielen Nutzern einer Kaffeeküche ermöglicht, selbstständig Produkte wie beispielsweise Kaffee abzurechnen. Dies erleichtert die Verwaltung der Kaffeeküche bzw. Kaffeekasse und gibt jedem Nutzer einen Überblick über seine Ausgaben und Einzahlungen.

Wesentliche Merkmale:
- **Digital** – Keine nervigen analogen Kaffeelisten mehr, aus denen die Ausgaben der Nutzer händisch ermittelt werden müssen.
- **Benutzerfreundlich**  – Schlanke Übersicht aller Nutzer durch schlichte Buttons und selbsterklärender Kaufprozess von Produkten.
- **Sicher** – Verwendung einer SQL-Datenbank für alle Daten des KKT bzw. der Nutzer. Ermöglicht das Sichern und Auslesen der Daten auch ohne die Software.
- **Einfach zu verwalten** – Vom Anlegen neuer Nutzer über das Aufladen von Guthaben auf ein Nutzerkonto bis hin zum Ein- und Austragen vorhandener Produkte ist alles innerhalb der Software möglich - ohne manuelle Interaktion mit der Datenbank.
- **Online** – Verantwortliche profitieren vom automatischen Erhalt von Statusmails über den Bestand von Produkten und Ereignissen im KKT.

<div align="center">
    
***-- Platzhalter: Foto von RPi + Touchscreen mit laufendem KKT (IAM-WK) --***
</div>

## Funktionen des KKT
Die Software startet mit einer Übersichtsseite, auf der alle aktiven Nutzer angezeigt werden. Diese kann als Hauptfenster betrachtet werden. Am unteren Rand dieser Seite befindet sich eine Leiste mit einem grünen Knopf (siehe Abbildung). Im Falle eines internen Fehlers springt dieser Knopf auf Rot. Über diesen Knopf kann ein Fenster geöffnet werden, das Informationen zur Software und deren Entwicklung bereitstellt. In dieser Leiste wird außerdem ein anstehender Geburtstag eines Nutzers angezeigt. Rechts davon befindet sich ein Button zum Anlegen eines neuen Nutzers.

<div align="center">
    
***-- Platzhalter: Screenshot der Übersichtsseite des KKT --***
</div>

Auf der Übersichtsseite werden die Nutzer in drei Gruppen eingeteilt. Diese Gruppen sind in der Software voreingestellt und heißen _Permanente_, _wissenschaftliche Mitarbeiter_ und _Studierende_. Andere Gruppennamen können bei Bedarf vergeben werden, indem der Code in `KKT_Main.py` angepasst wird.\
Neue Nutzer werden in einem separaten Fenster angelegt (siehe Abbildung). In diesem muss der Name des neuen Nutzers angegeben werden. Dieser muss sinnvoll gewählt werden und wird vor der Anlage des Nutzers überprüft. Des Weiteren wird der Name nach dem Anlegen des Nutzers formatiert. Falls vorhanden, wird der Vorname mit einem Punkt abgekürzt und folgt dem Nachnamen. Zudem muss eine Zuordnung zu einer Gruppe erfolgen. Nutzer der letzten Gruppe _Studierende_ müssen einen Betreuer angeben, sodass im Falle eines Ausscheidens des Nutzers eine Person für eventuell verbliebene Schulden geradestehen kann. Der Geburtstag kann angegeben werden, wenn dieser auf der Übersichtsseite erscheinen soll (freiwillig).

<div align="center">
    
***-- Platzhalter: Screenshot der Seite Nutzer Anlegen des KKT --***
</div>

Auf der Übersichtsseite können aktive Nutzer durch einen langen Klick gelöscht werden. Hierzu mindestens drei Sekunden lang den Button des jeweiligen Nutzers gedrückt halten (Zeitspanne kann in `KKT_Parameter.py` verändert werden). Falls mit dem Nutzer eine Abrechnung des Guthabens / der Schulden stattgefunden hat, kann dies beim Löschen angegeben werden. Gelöschte Nutzer werden automatisch in der Datenbank archiviert und können so später reaktiviert werden.\
Durch einen einfachen Klick auf einen Nutzer wird die Bestellübersicht geöffnet. Oben links wird der Name des Nutzers angezeigt und es wird die Möglichkeit geboten, einen Doktortitel zu erwerben (Spaß-Feature). Zudem wird der aktuelle Kontostand angezeigt. Über zwei Buttons besteht die Möglichkeit, die letzten Käufe in einem Kontoauszug anzuzeigen und das Konto aufzuladen.

<div align="center">
    
***-- Platzhalter: Screenshot der Seite Bestellübersicht des KKT --***
</div>

Im Fenster der Bestellübersicht können Produkte für den Kauf ausgewählt werden.

<div align="center">
    
***… Platzhalter: weitere Beschreibung folgt noch ...***
</div>

## Installation (auf Raspberry Pi)
### Notwendige Pakete bzw. Python-Bibliotheken
Wenn KKT auf einem Raspberry Pi mit Touchscreen installiert werden soll, muss dieser zunächst vollständig mit einer Desktopumgebung eingerichtet werden. KKT benötigt verschiedene Pakete bzw. Python-Bibliotheken, die installiert sein müssen:
- **GTK 3.0** – In der Regel in Raspbian / Raspberry Pi OS enthalten.
- **Python3.x** – In der Regel in Raspbian / Raspberry Pi OS enthalten.
- **python3-gi-cairo** – Für die Darstellung der Diagramme im KKT.
```
sudo apt-get install python3-gi-cairo
```
- **python3-numpy** – Für die Erstellung der Diagramme.
```
sudo apt-get install python3-numpy
```
- **python3-matplotlib** – Ebenfalls für die Erstellung der Diagramme.
```
sudo apt-get install python3-matplotlib
```
- **unclutter** (optional) – Lässt den Mauszeiger verschwinden. Funktioniert allerdings mit dem neuen Raspberry Pi OS nicht mehr. Grund hierfür ist der Wechsel auf Wayland.
```
sudo apt-get install unclutter
```
- **xscreensaver** (optional) – Vermeidet einen [Sperrbildschirm](https://stackoverflow.com/questions/30985964/how-to-disable-sleeping-on-raspberry-pi), der bei Berührung im Hintergrund einen Klick ausführt. Funktioniert unter Umständen mit dem neuen Raspberry Pi OS nicht mehr.
```
sudo apt-get install xscreensaver
```

### Starten der Software
KKT kann entweder über die Konsole im Ordner der Software mit dem Befehl
```
sudo python3.x KKT_Main.py
```
gestartet werden, wobei `x` für die installierte Python-Version steht. Alternativ kann ein einfaches Bash-Skript auf dem Desktop platziert werden, das durch einen Klick die Software startet. Beispielhafter Code für das Bash-Skript:
```
!/bin/bash
cd Pfad
sudo python3.x ./KKT_Main.py
```
Dabei ist die Bezeichnung `Pfad` durch den Pfad zum selbst angelegten Ordner mit allen Daten des KKT zu ersetzen.
Wichtig: Das KKT muss innerhalb einer laufenden grafischen Benutzeroberfläche gestartet werden.

Sollte KKT zu diesem Zeitpunkt noch nicht starten, könnte das an weiteren fehlenden Paketen liegen. In diesem Fall müssen die noch fehlenden Pakete anhand der Fehlermeldungen identifiziert und installiert werden.

### Tipp: Server für Backups
Die Einrichtung eines Servers, der es ermöglicht, einen Ordner auf dem Gerät (Raspberry Pi) als Netzwerklaufwerk auf einem anderen Gerät zu nutzen, kann praktisch sein, wenn es um das Erstellen von (automatischen) Backups der Datenbank geht. Hierfür kann beispielsweise ein Samba-Server eingesetzt werden. Es wird empfohlen regelmäßige Backups von der SQL-Datenbank `KKT_database.sqlite` anzulegen.

## Aufbau des KKT
Die Software besteht aus den einzelnen Python-Dateien `KKT_Main.py`, `KKT_Parameter.py`, `KKT_Verwaltung.py`, `GUIElemente.py` und `DBVerwaltung.py`. Zudem sind die beiden Dateien `KKT_GUI.glade` und `GUITastatur.glade` enthalten aus denen die grafische Benutzeroberfläche aufgebaut wird. Des Weiteren existiert die Datenbank `KKT_database.sqlite` für alle Daten des KKT bzw. der Nutzer sowie einige Bilder `KKT_img_Warning.png`, `KKT_img_Purchased.png`, `KKT_img_Stop.png`, `KKT_img_Logo.png`, `KKT_img_QRCode.png`, die innerhalb der Software dargestellt werden. Für den Verantwortlichen der Kaffeeküche sind nur die folgenden Dateien von Interesse:
- `KKT_Main.py`
- `KKT_Parameter.py`
- `KKT_database.sqlite`
- `KKT_img_QRCode.png`

Zum Starten der Software muss `KKT_Main.py` aufgerufen werden (s. [Oben](#Starten-der-Software)). `KKT_Parameter.py`, `KKT_database.sqlite` und `KKT_img_QRCode.png` müssen einmalig an die Bedürfnisse der Kaffeeküche bzw. des Verantwortlichen angepasst werden (s. [Unten](#Anpassungen-vor-Start)).\
Der Code des KKT ist hauptsächlich in der Datei `KKT_Main.py` zu finden. Für Entwickler ist diese Datei die interessanteste (erste) Anlaufstelle. In der Datei `KKT_Parameter.py` sind alle relevanten Variablen ausgelagert. In den übrigen Python-Dateien sind einzelne Funktionen zu finden. Dazu gehören beispielsweise die Interaktion mit der Datenbank und die Bereitstellung einer Bildschirmtastatur. Die beiden Glade-Dateien `KKT_GUI.glade` und `GUITastatur.glade` wurden mit der Software _Glade 3.40.0_ erstellt und können mit dieser Software auch wieder verändert bzw. weiterentwickelt werden. In diesen Dateien befinden sich in XML die Informationen vieler GUI-Elemente wie Buttons oder Labels. Der Aufbau der Datenbank `KKT_database.sqlite` wird in einem separaten Kapitel erläutert (s. [Unten](#Aufbau-der-Datenbank)).

## Anpassungen vor Start
### Parameterdatei
Die Datei `KKT_Parameter.py` muss einmalig an die Bedürfnisse der jeweiligen Kaffeeküche bzw. des Verantwortlichen angepasst werden. Die Variablen in der Datei sind in drei Kategorien eingeteilt:  1. Variablen, die die nach außen gerichtete Funktionalität für Nutzer steuern, 2. Variablen, die eher die interne Funktionalität steuern, 3. Variablen, die nur für Entwickler von Interesse sind. Alle Variablen sind kommentiert, sodass die Zuordnung einfach möglich sein dürfte. Folgende Variablen sollten beachtet bzw. angepasst werden:
- Maximaler Schuldenstand eines Nutzers
- Gutschrift für das Ausräumen einer Spülmaschine (als Motivation gedacht)
- Nach welcher Zeitspanne diese Gutschrift wieder abgerufen werden kann
- Der Preis für den Kauf eines Doktortitels (Spaß-Feature)
- Die Staffelungen der Beträge, um die das Konto eines Nutzers aufgeladen werden kann
- Die Bankdaten einer Kaffeeküche bzw. eines Verantwortlichen
- Nach welcher Zeitspanne ein Nutzer als inaktiv markiert wird

Wenn das Feature zum automatischen Versenden von Statusmails genutzt werden soll (s. [Unten](#Statusmails)), muss es aktiviert werden (die entsprechende Variable muss auf `True` gesetzt werden) und die Informationen zum angelegten Mailkonto müssen in den weiteren entsprechenden Variablen gespeichert werden.

### Datenbank
Die mitgelieferte Datenbank `KKT_database.sqlite` enthält Beispieldaten in allen zum Programmstart erforderlichen Tabellen und kann somit sofort verwendet werden. Es ist allerdings sinnvoll, die Datenbank an die Bedürfnisse der Kaffeeküche bzw. des Verantwortlichen anzupassen. Hierfür kann beispielsweise die Software _DB Browser for SQLite_ verwendet werden.\
In der Tabelle `Nutzer`, die alle aktiven Nutzer des KKT enthält, können die exemplarischen Personen wie _Einstein_ entfernt werden und alle aktiven Nutzer einer Kaffeeküche zum Start hinzugefügt werden. Jeder Nutzer hat einen `Namen`, einen `Kontostand`, einen `Rang`, einen `Geburtstag` (optional) und eine `letzte Aktivität`. Beispielsweise kann der Nutzer _M. Müller_ mit einem _Kontostand von 0_, einem _Rang von 0_ (mögliche Werte sind 0, 1 oder 2, die darüber entscheiden, in welcher Gruppe er angezeigt wird), einem _Geburtstag von 31.8.1995_ (als STRING eingeben) und einer _letzten Aktivität von 2025-01-20 09:15:00_ (ebenfalls als STRING eingeben) angelegt werden. Es ist natürlich auch möglich, die aktiven Nutzer erst später im KKT anzulegen (s. [Oben](#Funktionen-des-KKT)). Der Nutzer _Gästekonto_ (für alle Nutzer gedacht) sollte nicht entfernt werden, während der Nutzer _Diebstahlkonto_ nicht entfernt werden darf, da die Software sonst nicht ordnungsgemäß funktioniert. 
In der Tabelle `Bestand` müssen die Produkte angelegt werden, die in der Kaffeeküche verkauft werden sollen. Jedes Produkt hat einen `Namen`, einen `Bestand`, eine `Variable für die Aktivität`, einen `Sollbestand` und einen `Preis`. Beispielsweise kann das Produkt _Kaffee_ mit einem _Bestand von 50_ (genug Bohnen für 50 Tassen Kaffee vorhanden), einem _Sollbestand von 20_ (mindestens 20 Tassen Kaffee sollten immer zur Verfügung stehen), und einem _Preis von 0,3_ (Einheit Euro) angelegt werden. Mit einer _Aktivität von 0_ wird das Produkt im KKT angezeigt. Produkte mit einer _Aktivität von 1_ werden nicht angezeigt.

### QR-Code
Wenn ein Bankkonto für die Kaffeeküche existiert, kann für eine schnelle Überweisung ein QR-Code angelegt (siehe eigene Banking-App) und im KKT angezeigt werden. Der QR-Code muss hierfür in der Datei `KKT_img_QRCode.png` gespeichert sein. Die in diesem Beispielbild vorgegebene Auflösung darf hierbei nicht verändert werden!

### Statusmails
Ein besonderes Feature des KKT ist das automatische Versenden von Statusmails. In diesen E-Mails wird der noch vorhandene Bestand von Produkten mitgeteilt, sofern dieser unter einen festgelegten Grenzwert fällt. Zusätzlich werden die letzten Ereignisse des KKT angehängt. Es wird nur eine E-Mail pro Woche mit allen Informationen versendet. E-Mails, die Auskunft über den Bestand geben, können dagegen einmal pro Tag versendet werden.\
Um dieses Feature nutzen zu können, muss zunächst ein Mailkonto auf einem Mailserver angelegt werden, auf das per SMTP-Protokoll zugegriffen werden kann. Zudem ist eine stabile Internetverbindung zum Gerät erforderlich, auf dem KKT läuft. In der Datei `KKT_Parameter.py` muss das Feature außerdem aktiviert und eingerichtet sein. Da es sich hierbei noch um ein experimentelles Feature handelt, wird bei auftretenden Problemen empfohlen, das Feature vorerst abzuschalten.

## Aufbau der Datenbank
Die Datenbank besteht aus fünf einzelnen Tabellen, die eine unterschiedliche Anzahl an Variablen enthalten. Die Struktur der Datenbank und die Funktion der Variablen sind in der folgenden Abbildung aufgeschlüsselt:

<img width="1248" height="2950" alt="Übersicht Datenbank" src="https://github.com/user-attachments/assets/4e7ba0b0-14c5-4a0d-b46f-760e37fb94b3" />

Die Tabellen `Nutzer` und `NutzerAlt` sind für die Speicherung von Nutzerdaten vorgesehen. Bei der Löschung eines Nutzers werden einige seiner Daten in die Tabelle `NutzerAlt` transferiert. In der Tabelle `Bestand` sind die Produkte gespeichert, die im KKT angezeigt und erworben werden können. Die Tabellen `Bestellung` und `Log` dienen der Auswertung bzw. Kontrolle. In `Bestellung` werden alle Bestellungen / Käufe von Nutzern protokolliert und in `Log` sind Systemmeldungen bzw. Ereignisse protokolliert, die für eine Fehlersuche oder das Auffinden einer Manipulation herangezogen werden können. Folgende Ereignisse werden protokolliert:
- Neustart der Software
- Anlegen eines neuen Nutzers
- Löschen eines Nutzers (+ Kontostand wurde auf Null gesetzt)
- Kauf eines Doktortitels durch einen Nutzer
- Einzahlung von Geld auf das Konto eines Nutzers
- Änderung des Bestands eines Produkts (+ Angaben zur Art der Änderung)
- Auftreten eines Fehlers im Thread InterneVerwaltung (+ Art des Fehlers)
- Der Wochenumsatz der letzten Kalenderwoche

## Beitragende
Bis Version 1.8 vom 27. April 2025:\
Komplett designt, programmiert und veröffentlicht von _Anselm Lennard Heuer_

## Lizenz
KKT ist Open-Source und lizenziert unter der [GNU General Public License v3.0](https://github.com/AnselmSoftware/KKT/blob/main/LICENSE).
