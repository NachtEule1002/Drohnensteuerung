# Dashboard über Pygame realisieren
# Hier KLASSE!!!
#---------------------------------------------------


import pygame
import sys
import dronecomms
import main

class dashboard():

    # Fenster erstellen und starten
    def __init__(self, droneobject):
        self.drone = droneobject
        pygame.init()                                           
        self.screen = pygame.display.set_mode((1500, 1000))  
        pygame.display.set_caption("Dashboard Drohnensteuerung")


    # Gucken ob Fenster geschlossen werden soll
    def checkForExit(self):   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("EXIT")
                pygame.quit()
                main.quitApp()
                




    # Screenupdate
    def new():
        pygame.display.flip()




    # Bild anzeigen
    def showImage(self, img):
        self.screen.blit(img, (0,0))
        pygame.display.flip()