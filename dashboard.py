# Dashboard über Pygame realisieren
# Hier KLASSE!!!!
#---------------------------------------------------


import pygame
import sys
import dronecomms



class dashboard(object):

    width = 1600
    hight = 1200
    TEXTCOLOR = (0, 0, 0)
    BACKGROUNDCOLOR = None
    CAMERAPOS = (0,0)

    # Fenster erstellen und starten
    def __init__(self, droneobject):
        if droneobject != False:
            self.drone = droneobject
        pygame.init()                                          
        self.screen = pygame.display.set_mode((dashboard.width, dashboard.hight))
        self.screen.fill((255,255,255)) 
        pygame.display.set_caption("Drohnensteuerung")
        self.FONT = pygame.font.SysFont("arial", 60, False, False)
        self.rect1 = pygame.Rect(dashboard.CAMERAPOS, (500,500))
        


    # Screenupdate
    def update(self):
        pygame.display.flip()

    def showText(self, text, x, y):
        img = self.FONT.render(text, True, dashboard.TEXTCOLOR, dashboard.BACKGROUNDCOLOR)
        self.screen.blit(img, (x, y))

    # Bild anzeigen
    def showImage(self, img):
        self.screen.blit(img, dashboard.CAMERAPOS)

    # Höhenanzeige
    def showHeight(self, height):
        self.screen.blit(str(height), (0,0))

    #Alle Grafiken initialisieren
    def loadAll(self):
        self.showText("Test", 1200, 800)
        #pygame.draw.rect(self.screen, (0,0,0), self.rect1)