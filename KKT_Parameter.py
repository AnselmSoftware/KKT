"""
Created on 25.12.2024
@author: Anselm Heuer
Version 1.5 - last change on 12.09.2025
Enthaelt alle relevanten Parameter fuer das Kaffeekassentool - fuer Admins gedacht!
--Contains all relevant parameters for the coffee tool - intended for admins!--
"""
# This file contains all relevant parameters that influence the functionality of the coffee tool.
# Some of these affect the display of certain elements or labels, but some also affect how the tool works.
# A short description is given for each parameter, as well as any information on which values the parameter may / can assume.

# --- Parameter 1: Functionality of user interaction (Intended for administrators)
GUI_F1_MaxSchulden = -60            # Maximum possible debt amount of a user (in euros). No further purchases can be made above this amount.
GUI_F1_SpuelGutschrift = 0.30       # Amount credited to the user for cleaning out the dishwasher (in euros).
GUI_F1_SpuelFreigabezeit = 4        # After this period of time, the amount for cleaning out the dishwasher can be called up again (in hours).
GUI_F1_KontoAufladen_Betrag = {"BeID1": 5,                          # With these fixed amounts, a user can deposit money into their account (in euros).
                               "BeID2": 10,
                               "BeID3": 20,
                               "BeID4": 50}
GUI_F1_KontodatenAdmin = {"Inhaber": "Christine Lagarde",           # Enter the account details to be displayed in the coffee tool here.
                          "IBAN": "DE00 0000 0000 0000 0000 00",    # The QR code (.jpg) for the account details must be in the same folder.
                          "Bankleitzahl": "BLZ 000 000 00",
                          "Bankinstitut": "Bank"}
GUI_F1_NutzerInaktivTage = 30 * 3   # The period of time after which a user is no longer considered active and is marked (in days).
GUI_F1_KontoauszugTage = 30         # The period of time which purchases are displayed on the account statement (in days).
GUI_F1_GeburtstagTage = 5           # Birthdays of users before or after this time period based on the current day are displayed in the main window (in days).
GUI_F1_DrTitelKosten = 5            # Cost of the humorous purchase of a doctorate (in euros). Will be attached to the name after purchase.
GUI_F1_NutzerKategorieBezeichnung_1 = "Permanente"          # Name of the first user category in the main window (see tabs).
GUI_F1_NutzerKategorieBezeichnung_2 = "Wiss. Mitarbeiter"   # Name of the second user category in the main window (see tabs).
GUI_F1_NutzerKategorieBezeichnung_3 = "Studierende"         # Name of the third user category (these users require a supervisor) in the main window (see tabs).

# --- Parameter 2: Functionality internal to the software
# Should mails be written to the mail address (see below)? → Then set to True.
GUI_F2_MailSchreibenStatus = False                      # Switch to allow or prohibit “Write mails”.
GUI_F2_MailServer = "smtp.test.com"                     # Name of the mail server via which messages can be sent.
GUI_F2_MailAdresse = "KaffeekasseKKT@test.com"          # Messages are sent via this mail account.
GUI_F2_MailPasswort = "Password"                        # Password for the mail account.
GUI_F2_MailEmpfaenger = "Christine.Lagarde@test.com"    # The message containing the stock reports is sent to this e-mail address.
# Name of the file containing a database with the data of users, products, ... ...
# The tables Bestand, Bestellung, Nutzer, NutzerAlt and Log must exist in the database. You can use the dummy database as a guide.
GUI_F2_DatenbankDatei = "KKT_database.sqlite"
GUI_F2_GUIElementsDatei = "KKT_GUI.glade"               # Name of the file that contains all prefabricated GUI elements.
GUI_F2_WarnungIamge = "KKT_img_Warning.png"             # Name of the image that shows a warning symbol.
GUI_F2_GekauftIamge = "KKT_img_Purchased.png"           # Name of the image that shows a symbol for purchase.
# In which time period is the stock and status of the mail checked?
# In addition, it is checked during this period whether birthdays need to be displayed.
# Time period should reasonably be within a few seconds to minutes.
GUI_F2_VerwaltungInterval = 30                          # The period of time between internal processes (in seconds).
# If the button for a product is pressed for this period of time, the window for adjusting the stock is opened.
GUI_F2_ButtonProduktPressedZeitspanne = 2               # The period of time for the functionality (in seconds).
# If the button for a user is pressed for this period of time, the window for deleting a user is opened.
GUI_F2_ButtonNutzerPressedZeitspanne = 3                # The period of time for the functionality (in seconds).
# After purchasing products, the order overview is displayed for a certain period of time so that the user can check their purchase.
GUI_F2_BestellabschlussZeitspanne = 2                   # The period of time for the functionality (in seconds).
GUI_F2_AufloesungBreite = 800                           # Resolution setting - Width of the main window (in pixels).
GUI_F2_AufloesungHoehe = 480                            # Resolution setting - Height of the main window (in pixels).

# --- Parameter 3: Presentation of the coffee tool (Only intended for developers)
GUI_F3_Vollbild = True                                           # Full screen mode corresponds to True. Conveniently change to False for debugging.
GUI_F3_LinkGitHub = "https://github.com/AnselmSoftware/KKT.git"  # Link to the project page of the coffee tool on GitHub.
GUI_F3_Version = 1.9                                             # Version number of the entire coffee tool (not for individual files).
GUI_F3_Version_Date = "September 12, 2025"                       # Date on which this version was published.
GUI_F3_Copyright = "2019-2025 Anselm Lennard Heuer"              # Copyright info - Do not remove names, only add them if the coffee tool has been further developed.
