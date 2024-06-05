#-------------------------------------------------------------------------------------
# MAIN
#-------------------------------------------------------------------------------------

from djitellopy import tello
import pygame
import sys
import KeyboardControl
import XBoxControl
import os
import time
from inputs import get_gamepad
#-------------------------------------------------------------------------------------
# VARIABLEN
#-------------------------------------------------------------------------------------

# Großgeschrieben = Feste Variablen
DROHNE_AKTIV = False
#EINGABEMODUS = "xbox" # xbox oder key

running = True

controller = XBoxControl.XboxController()

#-------------------------------------------------------------------------------------
# METHODEN
#-------------------------------------------------------------------------------------

# Gucken ob Fenster geschlossen werden soll
def checkForExit():   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            tello.land()
            sys.exit()


# Ausgabefenster clearen:

clear = lambda: os.system('cls' if os.name=='nt' else 'clear') #direkt für Windows und Linux implementiert

#-------------------------------------------------------------------------------------

if DROHNE_AKTIV: #Nur wenn Drohne aktiv
    tello = tello.Tello()
    tello.connect()
    print(tello.get_battery())
#tello.streamon()

pygame.init()
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
pygame.display.set_caption("Drohnensteuerung")

#-------------------------------------------------------------------------------------
# HAUPTSCHLEIFE
#-------------------------------------------------------------------------------------



while running:

    clear()

    checkForExit()


    # Steuerungsstandard: [Eingabe gegeben, Hoch + Runter, Drehen Uhrzeigersinn + Gegenuhrzeigersinn, Vorwärts + Rückwärts, Rechts + Links, starten, landen, Button3, Button4]
    # [False oder True, -100 bis 100, -100 bis 100, -100 bis 100, -100 bis 100, 0 und 1, 0 und 1, 0 und 1, 0 und 1]

    #if EINGABEMODUS == "key":
        #Daten von Tastatur
    KeyboardDaten = KeyboardControl.keyboardControl()

    #else:
        #Daten von Controller
    
    
    ControllerDaten = controller.read()

    SteuerungsDaten = [0,0,0,0,0,0,0,0]
    
    if KeyboardDaten[0] == 1:
        print("Nutze Keyboard")
        SteuerungsDaten = KeyboardDaten[1:9]
    else:
        print("Nutze Controller")
        #print(ControllerDaten)
        SteuerungsDaten = ControllerDaten[1:9]
    
    print(SteuerungsDaten)

    # Hier die Daten in Bewegungsbefehle
        
    #pygame.display.update()
    #clock.tick(60)

    time.sleep(0.01)
    