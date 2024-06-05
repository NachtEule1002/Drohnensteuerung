#-------------------------------------------------------------------------------------
# MAIN
#-------------------------------------------------------------------------------------

from djitellopy import tello
import pygame
import sys
import KeyboardControl
#-------------------------------------------------------------------------------------
# VARIABLEN
#-------------------------------------------------------------------------------------

# Großgeschrieben = Feste Variablen
DROHNE_AKTIV = False
EINGABEMODUS = "xbox" # xbox oder key

running = True

#-------------------------------------------------------------------------------------
# METHODEN
#-------------------------------------------------------------------------------------

# Gucken ob Fenster geschlossen werden soll
def checkForExit():   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            tello.land()
            sys.exit()


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

    checkForExit()

    # Steuerungsstandard: [Eingabe gegeben, Hoch + Runter, Drehen Uhrzeigersinn + Gegenuhrzeigersinn, Vorwärts + Rückwärts, Rechts + Links, starten, landen, Button3, Button4]
    # [0 und 1, -100 bis 100, -100 bis 100, -100 bis 100, -100 bis 100, 0 und 1, 0 und 1, 0 und 1, 0 und 1]

    if EINGABEMODUS == "key":
        #Daten von Tastatur
        KeyboardControl.keyboardControl()
    #else:
        #Daten von Controller


    # Hier die Daten in Bewegungsbefehle
        
    #pygame.display.update()
    #clock.tick(60)