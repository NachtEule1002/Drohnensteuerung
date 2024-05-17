#-------------------------------------------------------------------------------------
# MAIN
#-------------------------------------------------------------------------------------

from djitellopy import tello
import pygame
import sys
import KeyboardControl
#-------------------------------------------------------------------------------------
# VARIABLEN

running = True

#-------------------------------------------------------------------------------------
# METHODEN

# Gucken ob man Fenster schließen will
def checkForExit():   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            tello.land()
            sys.exit()


#-------------------------------------------------------------------------------------
            
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

while running:

    checkForExit()

    KeyboardControl.keyboardControl()
        
    #pygame.display.update()
    #clock.tick(60)