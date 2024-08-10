# -------------------------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------------------------

from djitellopy import tello
import pygame
import KeyboardControl
import XBoxControl
import os
import time
from inputs import get_gamepad
import socket
import dronecomms
import dashboard
import ImageProcessing
import sys
from pythonping import ping
# -------------------------------------------------------------------------------------
# VARIABLEN
# -------------------------------------------------------------------------------------

# Großgeschrieben = Feste Variablen

DRONE_IP = '192.168.10.1'

AUSGABEARRAY = []


# Initialer Check, ob Drohne verbunden ist

out = ping(DRONE_IP, count=1, verbose=True)

if "Request timed out" in str(out):
    print("Drohne nicht verbunden")
    AUSGABEARRAY.append("Drohne nicht verbunden")
    DROHNE_AKTIV = False
else:
    print("Drohne verbunden")
    AUSGABEARRAY.append("Drohne verbunden")
    DROHNE_AKTIV = True


running = True

controller = XBoxControl.XboxController()


# -------------------------------------------------------------------------------------
# METHODEN
# -------------------------------------------------------------------------------------
            
# Exit

def checkForExit():   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global running
            pygame.quit()
            if DROHNE_AKTIV:
                drone.land()
            running = False
            print("EXIT")
            sys.exit()

    
    

# Ausgabefenster clearen:

clear = lambda: os.system('cls' if os.name=='nt' else 'clear') #direkt für Windows und Linux implementiert

# -------------------------------------------------------------------------------------

if DROHNE_AKTIV: # Nur wenn Drohne aktiv
    drone = dronecomms.dronecomms()
    drone.connect()
    drone.getBattery()
    drone.streamon()
    dashboard = dashboard.dashboard(drone)
else:
    dashboard = dashboard.dashboard(False)
    

# -------------------------------------------------------------------------------------
# HAUPTSCHLEIFE
# -------------------------------------------------------------------------------------
'''
X=600
Y = 600
scrn = pygame.display.set_mode((X, Y))
'''

while running:

    #clear()
    print(AUSGABEARRAY)
    

    checkForExit()



    # height = drone.getheight()
    # dashboard.showHeight(height)
    
    # dashboard.all()
    pygame.display.flip()

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
        print(ControllerDaten)
        SteuerungsDaten = ControllerDaten[1:9]
    
    #print(SteuerungsDaten)
    #print("Hallo")

    if DROHNE_AKTIV:

        currentImg = drone.getImage()
        dashboard.showImage(currentImg)

        print("Batterie-Ladestand: " + str(drone.getBattery()) + "%")
        print("vx: "+str(drone.getspeed("x")) + " vy: " + str(drone.getspeed("y")) + " vz: " + str(drone.getspeed("z")))
        drone.sendcontrols(SteuerungsDaten)

    time.sleep(1/15)