# Dashboard über Pygame realisieren
# Hier KLASSE!!!
#---------------------------------------------------


import pygame
import sys
import dronecomms


class dashboard():

    # Fenster erstellen und starten
    def __init__(self, droneobject):
        if droneobject != False:
            self.drone = droneobject
        pygame.init()                                           
        self.screen = pygame.display.set_mode((1500, 1000))  
        pygame.display.set_caption("Dashboard Drohnensteuerung")


    # Gucken ob Fenster geschlossen werden soll
    
                
                




    # Screenupdate
    def new():
        pygame.display.flip()




    # Bild anzeigen
    def showImage(self, img):
        self.screen.blit(img, (0,0))
        pygame.display.flip()