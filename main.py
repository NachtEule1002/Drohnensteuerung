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
    

# Ausgabefenster clearen:

clear = lambda: os.system('cls' if os.name=='nt' else 'clear') #direkt für Windows und Linux implementiert

# -------------------------------------------------------------------------------------

if DROHNE_AKTIV: # Nur wenn Drohne aktiv
    drone = dronecomms.dronecomms()
    drone.connect()
    drone.getBattery()
    drone.streamon()
    dashboard = dashboard.Dashboard(drone)

else:
    dashboard = dashboard.Dashboard(False)
    print("Drohne schallert")

# -------------------------------------------------------------------------------------
# HAUPTSCHLEIFE
# -------------------------------------------------------------------------------------

#vid = cv2.VideoCapture(0)

videostatus = 0

count = 0
height = 0
bat = 0
temp = 0

while running:

    count = count + 1

    clear()
    print(AUSGABEARRAY)


    # Steuerungsstandard: [Eingabe gegeben, Hoch + Runter, Drehen Uhrzeigersinn + Gegenuhrzeigersinn, Vorwärts + Rückwärts, Rechts + Links, starten + Landen, Button2, Button3, Button4]
    # [False oder True, Modus, -100 bis 100, -100 bis 100, -100 bis 100, -100 bis 100, 0 und 1, 0 und 1, 0 und 1, 0 und 1]

    KeyboardDaten = KeyboardControl.keyboardControl()
    
    
    ControllerDaten = controller.read()

    SteuerungsDaten = [0,0,0,0,0,0,0,0]
    


    #ret, frame = vid.read()

    #currentImg = ImageProcessing.processImage(frame)

    if DROHNE_AKTIV:

        currentImg, BildsteuerDaten = ImageProcessing.processImage(drone.getImage(),videostatus)

        if count > 15:
            height = drone.getheight()
            bat = drone.getBattery()
            temp = drone.gettemperature()
            count = 0


        dashboard.loadall(currentImg, height, bat, temp, videostatus)


        # Hier abfragen, damit Bildsteuerung überstimmt wird
        if videostatus != 0 and (ControllerDaten[7] == 1 or KeyboardDaten[7] == 1):
            videostatus = 0
        elif videostatus != 1 and (ControllerDaten[8] == 1 or KeyboardDaten[8] == 1):
            videostatus = 1
        elif videostatus != 2 and (ControllerDaten[9] == 1 or KeyboardDaten[9] == 1):
            videostatus = 2
        elif videostatus != 3 and (ControllerDaten[10] == 1 or KeyboardDaten[10] == 1):
            videostatus = 3
        elif videostatus != 4 and (ControllerDaten[11] == 1 or KeyboardDaten[11] == 1):
            videostatus = 4

        print("Videostatus: " + str(videostatus))


        if KeyboardDaten[0] == 1:
            print("Nutze Keyboard")
            SteuerungsDaten = KeyboardDaten[1:9]
            steuerungsmodus = 1

        elif BildsteuerDaten[0] == 1:

            print("Nutze Bildsteuerung")
            SteuerungsDaten = BildsteuerDaten[2:10]
            steuerungsmodus = BildsteuerDaten[1]

        else:

            print("Nutze Controller")
            #print(ControllerDaten)
            SteuerungsDaten = ControllerDaten[1:9]
            steuerungsmodus = 1


        print(SteuerungsDaten)

        print("vx: "+str(drone.getspeed("x")) + " vy: " + str(drone.getspeed("y")) + " vz: " + str(drone.getspeed("z")))
        drone.sendcontrols(steuerungsmodus, SteuerungsDaten[0:6])






    time.sleep(1/15)