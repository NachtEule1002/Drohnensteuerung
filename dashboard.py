# Dashboard über Pygame realisieren
# Hier KLASSE!!!!
#---------------------------------------------------


import pygame
import sys
import dronecomms



class Dashboard(object):

    TEXTCOLOR = (0, 0, 0)
    TEXTBACKGROUNDCOLOR = (255, 255, 255)
    MARGINCOLOR = (0, 0, 0)
    BACKGROUNDCOLOR = (115, 179, 189)
    MARGIN = 5

    #GRAPHICS
    #Camera
    CAMERAPOS = 10, 10
    CAMERA = 960, 720
    CAMERATITLE = "Kamerabild"

    #Status
    STATUSPOS = 1000, 10
    STATUSAREA = 420, 400
    STATUSDISTANCE = 70

    #Battery
    BATTERYPOS = STATUSPOS[0] + 20, STATUSPOS[1] + STATUSDISTANCE

    #Height
    HEIGHTPOS = STATUSPOS[0] + 20, STATUSPOS[1] + 2*STATUSDISTANCE

    #Temperature
    TEMPERATUREPOS = STATUSPOS[0] + 20, STATUSPOS[1] + 3*STATUSDISTANCE

    #Max Resolution
    MAXRESOLUTION = 1920, 1080

    #BUTTONS
    mousepos = 0, 0
    mousepressed = False
    #Button Takeoff
    BUTTONTAKEOFFPOS = 1100, 1100

    # Fenster erstellen und starten
    def __init__(self, droneobject):
        if droneobject != False:
            self.drone = droneobject
        pygame.init()                                          
        window = pygame.display.get_desktop_sizes()
        window = window[0]
        windowwidth = window[0]
        windowheight = window[1]
        self.screen = pygame.display.set_mode((windowwidth-10, windowheight-70))
        pygame.display.set_caption("Dashboard Drohnensteuerung")
        self.FONT = pygame.font.SysFont("bahnschrift", 40, False, False)

        


        #EXTRA AREAS
        #Camera
        self.cameraarea = pygame.Rect(Dashboard.CAMERAPOS[0]-Dashboard.MARGIN, Dashboard.CAMERAPOS[1]-Dashboard.MARGIN, Dashboard.CAMERA[0]+2*Dashboard.MARGIN, Dashboard.CAMERA[1]+2*Dashboard.MARGIN)

        #Status
        self.statusarea = pygame.Rect(Dashboard.STATUSPOS[0]-Dashboard.MARGIN, Dashboard.STATUSPOS[1]-Dashboard.MARGIN, Dashboard.STATUSAREA[0]+2*Dashboard.MARGIN, Dashboard.STATUSAREA[1]+2*Dashboard.MARGIN)

        #Max Resolution
        self.maxresolution = pygame.Rect(Dashboard.MAXRESOLUTION[0], 0, 10, Dashboard.MAXRESOLUTION[1])

        #BUTTONS
        #Button Takeoff
        self.buttontakeoff = Button("Takeoff", Dashboard.BUTTONTAKEOFFPOS[0], Dashboard.BUTTONTAKEOFFPOS[1])



    def checkforevent(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #if pygame.mouse.get_pressed()[0] and not Dashboard.mousepressed:
            #print("Jooo")
            #Dashboard.mousepos = pygame.mouse.get_pos()
            #if self.button.get_rect().collidepoint(Dashboard.mousepos):
            #print("Takeoff")

            #Dashboard.mousepressed = True
            #if not pygame.mouse.get_pressed()[0]:
            #Dashboard.mousepressed = False




    def showText(self, text, x, y, margin):
        img = self.FONT.render(text, True, Dashboard.TEXTCOLOR, Dashboard.TEXTBACKGROUNDCOLOR)
        imgsize = pygame.font.Font.size(self.FONT, text)
        margin = pygame.Rect(x-margin, y-margin, imgsize[0]+2*margin, imgsize[1]+2*margin)
        pygame.draw.rect(self.screen, Dashboard.MARGINCOLOR, margin)
        self.screen.blit(img, (x, y))

    def checkbuttons(self):
        if self.buttontakeoff.ispressed():
            print("TAKEOFF")


    def loadall(self, img, height, battery, temperature):       #neuer parameter: videostatus
        self.screen.fill(Dashboard.BACKGROUNDCOLOR)
        Dashboard.checkforevent(self)
        Dashboard.checkbuttons(self)


        #if Dashboard.mousepos[0] >= Dashboard.BUTTONTAKEOFFPOS[0] and Dashboard.mousepos[0] <= (Dashboard.BUTTONTAKEOFFPOS[0]+100) and Dashboard.mousepos[1] >= Dashboard.BUTTONTAKEOFFPOS[1] and Dashboard.mousepos[1] <= (Dashboard.BUTTONTAKEOFFPOS[1]+100):
        # print("TAKEOFF")
        #Dashboard.mousepos = 0, 0

        #GRAPHICS
        #Camera
        pygame.draw.rect(self.screen, Dashboard.MARGINCOLOR, self.cameraarea)
        self.screen.blit(img, Dashboard.CAMERAPOS)
        self.showText(Dashboard.CAMERATITLE, Dashboard.CAMERAPOS[0], Dashboard.CAMERAPOS[1], Dashboard.MARGIN)

        #Battery
        self.showText("Batterie: " + str(battery) + " %", Dashboard.BATTERYPOS[0], Dashboard.BATTERYPOS[1], Dashboard.MARGIN)

        #Status
        pygame.draw.rect(self.screen, Dashboard.MARGINCOLOR, self.statusarea, Dashboard.MARGIN)
        self.showText("STATUS", Dashboard.STATUSPOS[0], Dashboard.STATUSPOS[1], Dashboard.MARGIN)

        #Height
        self.showText("Höhe: " + str(height) + " cm", Dashboard.HEIGHTPOS[0], Dashboard.HEIGHTPOS[1], Dashboard.MARGIN)

        #Temperature
        self.showText("Temperatur: " + str(temperature) + " °C", Dashboard.TEMPERATUREPOS[0], Dashboard.TEMPERATUREPOS[1], Dashboard.MARGIN)

        #Max Resolution
        pygame.draw.rect(self.screen, Dashboard.MARGINCOLOR, self.maxresolution)

        #BUTTONS
        #Button Takeoff
        self.buttontakeoff.showButton(self.screen)

        pygame.display.flip()

        #return videostatus


class Button:

    MARGIN = 5
    TEXTCOLOR = (0, 0, 0)
    TEXTBACKGROUNDCOLOR = (255, 255, 255)

    def __init__(self, text, x, y):
        FONT = pygame.font.SysFont("bahnschrift", 40, False, False)
        self.button = FONT.render(text, True, Button.TEXTCOLOR, Button.TEXTBACKGROUNDCOLOR)
        buttonsize = pygame.font.Font.size(FONT, text)
        self.margin = pygame.Rect(x-Button.MARGIN, y-Button.MARGIN, buttonsize[0]+2*Button.MARGIN, buttonsize[1]+2*Button.MARGIN)
        self.pressed = False

    def showButton(self, screen):
        pygame.draw.rect(screen, Dashboard.MARGINCOLOR, self.margin)
        screen.blit(self.button, (self.margin.x+Button.MARGIN, self.margin.y+Button.MARGIN))

    def ispressed(self):
        mousepos = pygame.mouse.get_pos()
        mousepressed = pygame.mouse.get_pressed()[0]
        if mousepressed and not self.pressed:
            if self.margin.collidepoint(mousepos):
                self.pressed = True
                return True
        if not mousepressed:
            self.pressed = False
        return False