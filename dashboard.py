# Dashboard über Pygame realisieren
# Hier KLASSE!!!
#---------------------------------------------------


import pygame
import sys

class dashboard():

    # Fenster erstellen und starten
    def __init__(self):
        pygame.init()                                           
        screen = pygame.display.set_mode((1500, 1000))  
        pygame.display.set_caption("Dashboard Drohnensteuerung")


    # Gucken ob Fenster geschlossen werden soll
    def checkForExit(self):   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #Hier noch Drohne landen, wenn Fenster geschlossen wird????
                pygame.quit()
                sys.exit()




    # Screenupdate
    def new():
        pygame.display.flip()





    # Image von Main bekommen
    #def show(img):
        #screen.blit(img, (0,0))