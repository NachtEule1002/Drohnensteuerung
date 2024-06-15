# Dashboard über Pygame realisieren
# Hier KLASSE!!!
#---------------------------------------------------


import pygame
import sys
import dronecomms


FONT = pygame.font.SysFont("arial", 60, False, False)
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = None



class dashboard():

    # Fenster erstellen und starten
    def __init__(self, droneobject):
        if droneobject != False:
            self.drone = droneobject
        pygame.init()                                          
        self.screen = pygame.display.set_mode((1500, 1000))
        self.screen.fill((255,255,255)) 
        pygame.display.set_caption("Dashboard Drohnensteuerung")
        


    # Screenupdate
    def new(self):
        pygame.display.flip()

    def showText(self, text, x, y):
        img = FONT.render(text, True, TEXTCOLOR, BACKGROUNDCOLOR)
        self.screen.blit(img ,(x,y))

    # Bild anzeigen
    def showImage(self, img):
        self.screen.blit(img, (0,0))

    # Höhenanzeige
    def showHeight(self, height):
        self.screen.blit(str(height), (0,0))