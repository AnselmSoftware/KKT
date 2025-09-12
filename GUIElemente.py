"""
Created on 18.12.2019
@author: Anselm Heuer
Version 1.6 - last change on 11.09.2025
Ein Sammlung von Widgets fuer eine GUI. Kann in eine bestehende GUI implementiert werden.
--A collection of widgets for a GUI. Can be implemented in an existing GUI--
--Comments in functions are partly written in German - can easily be translated into english with translation programs :)--
"""
# Import all relevant functions
import time
# modules for Gtk
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import GObject


class Widget_Produktanzeige(Gtk.Box):
    """
    Diese Klasse stellt ein Widget zur Verfuegung, dass aus einem Button und ein Label unter diesem Button besteht. Kann fuer die Anzeige eines Produkts
    in einer GUI verwendet werden. Es findet eine eigene kleine gekapselte Funktionalitaet statt, um zu erkennen, wie lange der Button gedrueckt wurde.
    Wird der Button laenger als eine bestimmte Zeitspanne gedruckt, wird ein Signal "ButtonXsPressed" emittet. Auch wird das Label unter dem Button rot
    gefaerbt, wenn die Zahl in dem Label dem Wert Null erreicht.

    Methoden:
    - [LeseID] Hiermit kann die eindeutige Identifikation des Widgets ausgelesen werden. Wird zur Laufzeit niemals veraendert.
    - [AnpassenLabelUnterButton] Hiermit kann die Zahl des Labels unter dem Button veraendert werden.
    - [BlinkenLabelUnterButton] Mit dieser Methode kann das Label unter dem Button kurz zum Aufblinken gebracht werden.
    """
    __gsignals__ = {'ButtonXsPressed': (GObject.SIGNAL_RUN_FIRST, None, (str, ))}

    def __init__(self, DimensionButton, MethodeBeiClick, WidgetID, LabelButton, LabelUnterButtonText, LabelUnterButtonZahl, PressedTimeMax):
        super().__init__(orientation=Gtk.Orientation(value=1))

        # Variablen dieser Klasse
        self.__ID = WidgetID  # Zur eindeutigen Identifikation des Widgets
        self.__LabelUnterButtonText = LabelUnterButtonText  # Z. B. nutzen, um den Bestand eines Produkts anzuzeigen. Ist der Text des Labels unter dem Button.
        self.__LabelUnterButtonZahl = LabelUnterButtonZahl  # Muss eine Zahl sein und wird dem Text __LabelUnterButtonText hinzugefuegt.
        self.__Blinker = 0
        self.__PressedTime = 0
        self.__PressedTimeMax = PressedTimeMax

        # Einzelne Widgets anlegen, die in diesem Widget gebuendelt verwendet werden:
        self.__Button = Gtk.Button(label="")
        self.__Button.get_child().set_markup("<b>{}</b>".format(LabelButton))
        self.__Label = Gtk.Label(label="")
        self.pack_start(self.__Button, False, True, 0)
        self.pack_start(self.__Label, False, True, 5)

        # Anpassen der Widgets
        self.__Button.set_size_request(DimensionButton[0], DimensionButton[1])
        self.__Button.connect("clicked", MethodeBeiClick, self)
        self.__Button.connect("pressed", self.__ZeitmessungButtonPressedStart)
        self.__Button.connect("released", self.__ZeitmessungButtonPressedEnde)
        self.__CheckeFarbeLabelUnterButton()

    def LeseID(self):
        return self.__ID

    def AnpassenLabelUnterButton(self, ZahlNeu):
        # Label unter dem Button (bzw. die Zahl innerhalb des Labels) wird veraendert
        if isinstance(ZahlNeu, int):
            self.__LabelUnterButtonZahl = ZahlNeu
            self.__CheckeFarbeLabelUnterButton()

    def BlinkenLabelUnterButton(self):
        # Das Label unter dem Button verschwindet und erscheint zweimal hintereinander wieder
        if self.__Blinker == 0:
            self.__Label.set_markup("")
            self.__Blinker += 1
        elif self.__Blinker == 1:
            self.__CheckeFarbeLabelUnterButton()
            self.__Blinker += 1
        elif self.__Blinker == 2:
            self.__Label.set_markup("")
            self.__Blinker += 1
        else:
            self.__CheckeFarbeLabelUnterButton()
            self.__Blinker = 0
            return False
        GLib.timeout_add(175, self.BlinkenLabelUnterButton)

    def __CheckeFarbeLabelUnterButton(self):
        # Es wird ueberprueft, ob die Farbe des Labels veraendert werden muss.
        # Entspricht __LabelUnterButtonZahl dem Wert Null, wird die Farbe des gesamten Labels auf Rot gesetzt
        if self.__LabelUnterButtonZahl <= 0:
            self.__Label.set_markup("<span color='red'>{}</span>".format(self.__LabelUnterButtonText + str(self.__LabelUnterButtonZahl)))
        else:
            self.__Label.set_label(self.__LabelUnterButtonText + str(self.__LabelUnterButtonZahl))

    def __ZeitmessungButtonPressedStart(self, GUIObjekt):
        # Wenn der Button gedrueckt wird, dann wird der Zeitpunkt abgespeichert
        self.__PressedTime = time.time()

    def __ZeitmessungButtonPressedEnde(self, GUIObjekt):
        # Wenn der Button nicht mehr gedrueckt wird, wird bestimmt, wie lange der Button insgesamt gedrueckt wurde.
        # Wurde der Button laenger als __PressedTimeMax gedruckt, dann wird ein Signal emittet.
        if time.time() - self.__PressedTime > self.__PressedTimeMax:
            self.emit("ButtonXsPressed", self.__ID)
        # print("Button wurde ", time.time() - self.__PressedTime, " s gedrueckt")


class Widget_NutzerButton(Gtk.Button):
    """
    Diese Klasse stellt einen angepassten Button zur Verfuegung, der um zwei Events erweitert ist. Es findet eine eigene kleine gekapselte
    Funktionalitaet statt, um zu erkennen wie lange der Button gedrueckt wurde. Wird der Button laenger als eine bestimmte Zeitspanne gedruckt,
    wird ein Signal "NutzerButtonXsPressed" emittet. Ansonsten wird nur das Signal "NutzerButtonClicked" emittet.

    Methoden:
    - [LeseID] Hiermit kann die eindeutige Identifikation des Widgets ausgelesen werden.
    - [SchreibeID] Hiermit kann die eindeutige Identifikation des Widgets neu geschrieben werden.
    """
    __gsignals__ = {'NutzerButtonXsPressed': (GObject.SIGNAL_RUN_FIRST, None, ()), 'NutzerButtonClicked': (GObject.SIGNAL_RUN_FIRST, None, ())}

    def __init__(self, DimensionButton, WidgetID, PressedTimeMax):
        super().__init__(label="")

        # Variablen dieser Klasse
        self.__ID = WidgetID
        self.__PressedTime = 0
        self.__PressedTimeMax = PressedTimeMax

        # Anpassen des Widgets
        self.set_size_request(DimensionButton[0], DimensionButton[1])
        self.connect("pressed", self.__ZeitmessungButtonPressedStart)
        self.connect("released", self.__ZeitmessungButtonPressedEnde)

    def LeseID(self):
        return self.__ID

    def SchreibeID(self, WidgetIDNeu):
        self.__ID = WidgetIDNeu

    def __ZeitmessungButtonPressedStart(self, GUIObjekt):
        # Wenn der Button gedrueckt wird, dann wird der Zeitpunkt abgespeichert
        self.__PressedTime = time.time()

    def __ZeitmessungButtonPressedEnde(self, GUIObjekt):
        # Wenn der Button nicht mehr gedrueckt wird, wird bestimmt, wie lange der Button insgesamt gedrueckt wurde.
        # Wurde der Button laenger als __PressedTimeMax gedruckt, dann wird ein spezielles Signal emittet. Ansonsten nur das Standardsignal "Klick".
        if time.time() - self.__PressedTime > self.__PressedTimeMax:
            self.emit("NutzerButtonXsPressed")
        else:
            self.emit("NutzerButtonClicked")
        # print("Button wurde ", time.time() - self.__PressedTime, " s gedrueckt")


class Widget_BetreuerButton(Gtk.ToggleButton):
    """
    Diese Klasse stellt einen angepassten ToggleButton zur Verfuegung, der eine eindeutige ID fuer den Namen des Betreuers besitzt.
    Weiterhin ist der ToggleButton aus optischen Gründen nicht fokusierbar.

    Methoden:
    - [LeseID] Hiermit kann die eindeutige Identifikation des Widgets ausgelesen werden.
    - [SchreibeID] Hiermit kann die eindeutige Identifikation des Widgets neu geschrieben werden.
    """
    def __init__(self, WidgetID):
        super().__init__(label="")

        # Variablen dieser Klasse
        self.__ID = WidgetID

        # Anpassen des Widgets
        self.set_can_focus(False)

    def LeseID(self):
        return self.__ID

    def SchreibeID(self, WidgetIDNeu):
        self.__ID = WidgetIDNeu


class Widget_BlinkerLabel(Gtk.Label):
    """
    Diese Klasse stellt ein angepasstes Label zur Verfuegung, dass in roter Schrift einen Text darstellt. Der Text kann auf Wunsch
    kurz aufblinken, um den Fokus eines Nutzers auf den Text zu lenken.

    Methoden:
    - [SchreibeLabel] Hiermit kann der Text des Labels / Widgets veraendert werden.
    - [BlinkenLabel] Mit dieser Methode kann der Text des Labels kurz zum Aufblinken gebracht werden.
    """
    def __init__(self, Label):
        super().__init__(label="")

        # Variablen dieser Klasse
        self.__Label = Label
        self.__Blinker = 0

        # Anpassen des Widgets
        self.set_markup("<span color='red'>{}</span>".format(self.__Label))

    def SchreibeLabel(self, LabelNeu):
        self.__Label = LabelNeu
        self.set_markup("<span color='red'>{}</span>".format(self.__Label))

    def BlinkenLabel(self):
        # Das Label verschwindet und erscheint zweimal hintereinander wieder
        if self.__Blinker == 0:
            self.set_markup("")
            self.__Blinker += 1
        elif self.__Blinker == 1:
            self.set_markup("<span color='red'>{}</span>".format(self.__Label))
            self.__Blinker += 1
        elif self.__Blinker == 2:
            self.set_markup("")
            self.__Blinker += 1
        else:
            self.set_markup("<span color='red'>{}</span>".format(self.__Label))
            self.__Blinker = 0
            return False
        GLib.timeout_add(175, self.BlinkenLabel)


class Widget_Tastatur(Gtk.Box):
    """
    Diese Klasse stellt eine digitale Tastatur als Widget zur Verfuegung, die bei ausreichend Platz in eine GUI integriert werden kann. Hierbei kann
    das Widget in einen Container (z. B. eine Gtk.Box) gepackt und danach ueber die Emitter-Signale genutzt werden. Die Emitter uebergeben das gedrueckte
    Zeichen einer Taste oder welche Funktionstaste gedrueckt wurde. Dabei werden Leerzeichen, Sonderzeichen und Buchstaben als "str" uebergeben, waehrend
    die Zahlen / Ziffern als "int" uebergeben werden. Die Tasten der Tastatur koennen nicht den Fokus erhalten, sodass "Entrys" oder andere Objekte,
    in die Text reingeschrieben werden soll, nicht den Fokus verlieren.

    Methoden:
    Anmerkung: Methoden nicht extern aufrufen, da hierfür nicht gedacht! - Lassen sich hier allerdings auch nicht kapseln (liegt an Gtk.Builder?!).
    """
    __gsignals__ = {'TastaturZahl': (GObject.SignalFlags.RUN_FIRST, None, (int, )), 'TastaturBuchstabe': (GObject.SignalFlags.RUN_FIRST, None, (str, )),
                    'TastaturSonderzeichen': (GObject.SignalFlags.RUN_FIRST, None, (str, )), 'TastaturBackspace': (GObject.SignalFlags.RUN_FIRST, None, ()),
                    'TastaturReturn': (GObject.SignalFlags.RUN_FIRST, None, ()), 'TastaturShift': (GObject.SignalFlags.RUN_FIRST, None, ()),
                    'TastaturTab': (GObject.SignalFlags.RUN_FIRST, None, ()), 'TastaturShiftLock': (GObject.SignalFlags.RUN_FIRST, None, (bool, ))}

    def __init__(self):
        super().__init__(orientation=Gtk.Orientation(value=1))

        # Builder erstellen und anpassen, um die einzelnen Widgets aus GUITastatur.glade auszulesen
        # Dieser Builder baut die vorgefertigte Tastatur auf und ueberfuehrt dies in Python-Code
        Builder = Gtk.Builder()
        Builder.add_from_file("GUITastatur.glade")
        Builder.connect_signals(self)  # Methoden aus GUITastatur.glade mit den Methoden in dieser Klasse verbinden
        self.__WindowTastatur = Builder.get_object("WindowTastatur")  # Alle benoetigten Widgets aus GUITastatur.glade als Variablen hier anlegen
        self.__BackspaceButton = Builder.get_object("buttonF1")
        self.__BackspaceButton.connect("pressed", self.__ButtonBackspacePressedStart)
        self.__BackspaceButton.connect("released", self.__ButtonBackspacePressedEnde)

        # Variablen, um Einstellungen und Zustaende fuer Tastatur zu speichern
        self.__ShiftAktiv = False
        self.__BackspaceAktiv = False
        self.__ListeBuchstaben = []
        for ButtonBuchstabe in range(10, 39):
            self.__ListeBuchstaben.append(Builder.get_object("button{}".format(ButtonBuchstabe)))

        self.pack_start(self.__WindowTastatur, False, True, 0)

    # ------------------------- Feature der Tastatur
    # ---------------------------------------------
    def __on_Backspace_clicked(self):
        self.emit("TastaturBackspace")
        if not self.__BackspaceAktiv:
            return False
        return True

    def __ButtonBackspacePressedStart(self, GUIButton):
        self.__BackspaceAktiv = True
        GLib.timeout_add(125, self.__on_Backspace_clicked)

    def __ButtonBackspacePressedEnde(self, GUIButton):
        self.__BackspaceAktiv = False

    def on_Return_clicked(self, GUIButton):
        self.emit("TastaturReturn")

    def on_Shift_clicked(self, GUIButton):
        self.emit("TastaturShift")

    def on_ShiftLock_clicked(self, GUIButton):
        if not self.__ShiftAktiv:
            self.__ShiftAktiv = True
            for ButtonBuchstabe in self.__ListeBuchstaben:
                ButtonBuchstabe.set_label(ButtonBuchstabe.get_child().get_text().upper())
        else:
            self.__ShiftAktiv = False
            for ButtonBuchstabe in self.__ListeBuchstaben:
                ButtonBuchstabe.set_label(ButtonBuchstabe.get_child().get_text().lower())
        self.emit("TastaturShiftLock", self.__ShiftAktiv)

    def on_Tab_clicked(self, GUIButton):
        self.emit("TastaturTab")

    def on_Spacebar_clicked(self, GUIButton):
        self.emit("TastaturSonderzeichen", " ")

    def on_Sonderzeichen_clicked(self, GUIButton):
        Sonderzeichen = GUIButton.get_child().get_text()
        self.emit("TastaturSonderzeichen", Sonderzeichen)

    def on_Zahl_clicked(self, GUIButton):
        Zahl = int(GUIButton.get_child().get_text())
        self.emit("TastaturZahl", Zahl)

    def on_Buchstabe_clicked(self, GUIButton):
        Buchstabe = GUIButton.get_child().get_text()
        self.emit("TastaturBuchstabe", Buchstabe)
