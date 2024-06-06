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
import socket
import dronecomms
#-------------------------------------------------------------------------------------
# VARIABLEN
#-------------------------------------------------------------------------------------

# Großgeschrieben = Feste Variablen

DRONE_IP = '192.168.10.1'
#DRONE_IP = '8.8.8.8'

AUSGABEARRAY = []

# Initialer Check, ob Drohne verbunden ist

ret = os.system("ping -n 1 " + DRONE_IP + " -w 100")
if ret != 0:
    print("Drohne nicht verbunden")
    AUSGABEARRAY.append("Drohne nicht verbunden")
    DROHNE_AKTIV = False
else:
    print("Drohne verbunden")
    AUSGABEARRAY.append("Drohne verbunden")
    DROHNE_AKTIV = True
    

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
            tello.end()


# Ausgabefenster clearen:

clear = lambda: os.system('cls' if os.name=='nt' else 'clear') #direkt für Windows und Linux implementiert

#-------------------------------------------------------------------------------------

if DROHNE_AKTIV: #Nur wenn Drohne aktiv
    tello = tello.Tello()
    tello.connect()
    #print("hallo")
    print(tello.get_battery())
    tello.streamon()
    dronecommunication = dronecomms.dronecomms(tello)

pygame.init()
screen = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()
pygame.display.set_caption("Drohnensteuerung")

#-------------------------------------------------------------------------------------
# HAUPTSCHLEIFE
#-------------------------------------------------------------------------------------
'''
X=600
Y = 600
scrn = pygame.display.set_mode((X, Y))
'''
cnt = 1

while running:

    clear()
    print(AUSGABEARRAY)
    

    checkForExit()


    # Steuerungsstandard: [Eingabe gegeben, Hoch + Runter, Drehen Uhrzeigersinn + Gegenuhrzeigersinn, Vorwärts + Rückwärts, Rechts + Links, starten + Landen, Button2, Button3, Button4]
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
    '''
    if cnt > 100:
    
        print("versuche Bilder zu bekommen")
        frame_read = tello.get_frame_read()
        print("read hat funktioniert")
        time.sleep(1)

        imp = pygame.image.load(frame_read.frame).convert()

        scrn.blit(imp, (0,0))

        # Hier die Daten in Bewegungsbefehle

        pygame.display.flip()
    '''
    pygame.display.update()

    if DROHNE_AKTIV:
        print("Batterie-Ladestand: " + str(tello.get_battery()) + "%")
        print("vx: "+str(tello.get_speed_x()) + " vy: " + str(tello.get_speed_y()) + " vz: " + str(tello.get_speed_z()))
        dronecommunication.sendcontrols(SteuerungsDaten)
    
    clock.tick(60)

    time.sleep(0.1)

    cnt = cnt+1
    