# -------------------------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------------------------
import cv2
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
    print("Drohne schallert")

# -------------------------------------------------------------------------------------
# HAUPTSCHLEIFE
# -------------------------------------------------------------------------------------

#vid = cv2.VideoCapture(0)

videostatus = 0

while running:

    clear()
    print(AUSGABEARRAY)


    checkForExit()


    dashboard.update()

    # Steuerungsstandard: [Eingabe gegeben, Hoch + Runter, Drehen Uhrzeigersinn + Gegenuhrzeigersinn, Vorwärts + Rückwärts, Rechts + Links, starten + Landen, Button2, Button3, Button4]
    # [False oder True, -100 bis 100, -100 bis 100, -100 bis 100, -100 bis 100, 0 und 1, 0 und 1, 0 und 1, 0 und 1]

    KeyboardDaten = KeyboardControl.keyboardControl()
    
    
    ControllerDaten = controller.read()

    SteuerungsDaten = [0,0,0,0,0,0,0,0]
    


    #ret, frame = vid.read()

    #currentImg = ImageProcessing.processImage(frame)

    if DROHNE_AKTIV:
        print("ANGEKOMMEN")
        currentImg, BildsteuerDaten = ImageProcessing.processImage(drone.getImage(),videostatus)

        dashboard.showImage(currentImg)

        if videostatus == 0 and (ControllerDaten[7] == 1 or KeyboardDaten[7] == 1):
            videostatus = 1
        elif videostatus == 1 and (ControllerDaten[8] == 1 or KeyboardDaten[8] == 1):
            videostatus = 0

        if KeyboardDaten[0] == 1:
            print("Nutze Keyboard")
            SteuerungsDaten = KeyboardDaten[1:9]

        elif BildsteuerDaten[0] == 1:

            print("Nutze Bildsteuerung")
            SteuerungsDaten = BildsteuerDaten[1:9]

        else:

            print("Nutze Controller")
            #print(ControllerDaten)
            SteuerungsDaten = ControllerDaten[1:9]


        print(SteuerungsDaten)

        print("Batterie-Ladestand: " + str(drone.getBattery()) + "%")
        print("vx: "+str(drone.getspeed("x")) + " vy: " + str(drone.getspeed("y")) + " vz: " + str(drone.getspeed("z")))
        drone.sendcontrols(SteuerungsDaten)

    time.sleep(1/15)