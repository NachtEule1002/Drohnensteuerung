# DASHBOARD
#---------------------------------------------------

import pygame
import sys


class Dashboard:

    TEXTCOLOR = (0, 0, 0)
    TEXTBACKGROUNDCOLOR = (255, 255, 255)
    MARGINCOLOR = (0, 0, 0)
    BACKGROUNDCOLOR = (115, 179, 189)
    MARGIN = 5
    VERTICALELEMENTDISTANCE = 70

    #Drohne nicht verbunden
    NODRONEPOS = 100 , 100


    #Camera
    CAMERAPOS = 10, 10
    CAMERAAREA = 960, 720
    CAMERATITLE = "Kamerabild"

    #STATUS
    STATUSPOS = 1000, 10
    STATUSAREA = 420, 400

    #Battery
    BATTERYPOS = STATUSPOS[0] + 20, STATUSPOS[1] + VERTICALELEMENTDISTANCE

    #Height
    HEIGHTPOS = STATUSPOS[0] + 20, STATUSPOS[1] + 2*VERTICALELEMENTDISTANCE

    #Temperature
    TEMPERATUREPOS = STATUSPOS[0] + 20, STATUSPOS[1] + 3*VERTICALELEMENTDISTANCE

    #MODUS
    MODUSPOS = 1000, 450
    MODUSAREA = 420, 400


    #BUTTONS
    #Button Freier Modus
    FREIERMODUSPOS = MODUSPOS[0] + 20, MODUSPOS[1] + VERTICALELEMENTDISTANCE
    #Button Ball folgen (Absolut)
    BALLFOLGENABSOLUTPOS = MODUSPOS[0] + 20, MODUSPOS[1] + 2*VERTICALELEMENTDISTANCE
    #Button Ball folgen (cm)
    BALLVERFOLGENCMPOS = MODUSPOS[0] + 20, MODUSPOS[1] + 3*VERTICALELEMENTDISTANCE
    #Button Gesichtserkennung
    GESICHTSERKENNUNGPOS = MODUSPOS[0] + 20, MODUSPOS[1] + 4*VERTICALELEMENTDISTANCE



    #Max Resolution
    MAXRESOLUTION = 1920, 1080




    # Fenster erstellen und starten
    def __init__(self,drone):
        pygame.init()                                          
        window = pygame.display.get_desktop_sizes()
        window = window[0]
        windowwidth = window[0]
        windowheight = window[1]
        self.screen = pygame.display.set_mode((windowwidth-10, windowheight-70))
        pygame.display.set_caption("Dashboard Drohnensteuerung")
        self.FONT = pygame.font.SysFont("bahnschrift", 40, False, False)

        #Keine Drohne verbunden
        if not drone:
            while True:
                Dashboard.checkforexit(self)
                self.screen.fill(Dashboard.BACKGROUNDCOLOR)
                self.showText("Drohne nicht verbunden!!!", Dashboard.NODRONEPOS[0], Dashboard.NODRONEPOS[1], Dashboard.MARGIN)
                pygame.display.flip()



        #EXTRA AREAS
        #Camera
        self.cameraarea = pygame.Rect(Dashboard.CAMERAPOS[0]-Dashboard.MARGIN, Dashboard.CAMERAPOS[1]-Dashboard.MARGIN, Dashboard.CAMERAAREA[0]+2*Dashboard.MARGIN, Dashboard.CAMERAAREA[1]+2*Dashboard.MARGIN)

        #Status
        self.statusarea = pygame.Rect(Dashboard.STATUSPOS[0]-Dashboard.MARGIN, Dashboard.STATUSPOS[1]-Dashboard.MARGIN, Dashboard.STATUSAREA[0]+2*Dashboard.MARGIN, Dashboard.STATUSAREA[1]+2*Dashboard.MARGIN)

        #Modus
        self.modusarea = pygame.Rect(Dashboard.MODUSPOS[0]-Dashboard.MARGIN, Dashboard.MODUSPOS[1]-Dashboard.MARGIN, Dashboard.MODUSAREA[0]+2*Dashboard.MARGIN, Dashboard.MODUSAREA[1]+2*Dashboard.MARGIN)

        #Max Resolution
        self.maxresolution = pygame.Rect(Dashboard.MAXRESOLUTION[0], 0, 10, Dashboard.MAXRESOLUTION[1])

        #BUTTONS
        #Button Freier Modus
        self.freiermodus = Button("Freier Modus", Dashboard.FREIERMODUSPOS[0], Dashboard.FREIERMODUSPOS[1])
        #Button Ball folgen (Absolut)
        self.ballfolgenabsolut = Button("Ball folgen (Absolut)", Dashboard.BALLFOLGENABSOLUTPOS[0], Dashboard.BALLFOLGENABSOLUTPOS[1])
        #Button Ball folgen (cm)
        self.ballfolgencm = Button("Ball folgen (cm)", Dashboard.BALLVERFOLGENCMPOS[0], Dashboard.BALLVERFOLGENCMPOS[1])
        #Button Gesichtserkennung
        self.gesichtserkennung = Button("Gesichtserkennung", Dashboard.GESICHTSERKENNUNGPOS[0], Dashboard.GESICHTSERKENNUNGPOS[1])


    def checkforexit(self):
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


    def checkbuttons(self, videostatus):
        if videostatus == 0:
            self.freiermodus.MARGINCOLOR = Button.PRESSEDMARGINCOLOR
        else:
            self.freiermodus.MARGINCOLOR = Button.MARGINCOLOR
        if videostatus == 1:
            self.ballfolgenabsolut.MARGINCOLOR = Button.PRESSEDMARGINCOLOR
        else:
            self.ballfolgenabsolut.MARGINCOLOR = Button.MARGINCOLOR
        if videostatus == 2:
            self.ballfolgencm.MARGINCOLOR = Button.PRESSEDMARGINCOLOR
        else:
            self.ballfolgencm.MARGINCOLOR = Button.MARGINCOLOR
        if videostatus == 3:
            self.gesichtserkennung.MARGINCOLOR = Button.PRESSEDMARGINCOLOR
        else:
            self.gesichtserkennung.MARGINCOLOR = Button.MARGINCOLOR



        if self.freiermodus.ispressed():
            videostatus = 0
        elif self.ballfolgenabsolut.ispressed():
            videostatus = 1
        elif self.ballfolgencm.ispressed():
            videostatus = 2
        elif self.gesichtserkennung.ispressed():
            videostatus = 3
        return videostatus


    def loadall(self, img, height, battery, temperature, videostatus):       #neuer parameter: videostatus
        self.screen.fill(Dashboard.BACKGROUNDCOLOR)
        Dashboard.checkforexit(self)
        videostatus = Dashboard.checkbuttons(self, videostatus)


        #GRAPHICS
        #Camera
        pygame.draw.rect(self.screen, Dashboard.MARGINCOLOR, self.cameraarea)
        self.screen.blit(img, Dashboard.CAMERAPOS)
        self.showText(Dashboard.CAMERATITLE, Dashboard.CAMERAPOS[0], Dashboard.CAMERAPOS[1], Dashboard.MARGIN)

        #Status
        pygame.draw.rect(self.screen, Dashboard.MARGINCOLOR, self.statusarea, Dashboard.MARGIN)
        self.showText("STATUS", Dashboard.STATUSPOS[0], Dashboard.STATUSPOS[1], Dashboard.MARGIN)

        #Battery
        self.showText("Batterie: " + str(battery) + " %", Dashboard.BATTERYPOS[0], Dashboard.BATTERYPOS[1], Dashboard.MARGIN)

        #Height
        self.showText("Höhe: " + str(height) + " cm", Dashboard.HEIGHTPOS[0], Dashboard.HEIGHTPOS[1], Dashboard.MARGIN)

        #Temperature
        self.showText("Temperatur: " + str(temperature) + " °C", Dashboard.TEMPERATUREPOS[0], Dashboard.TEMPERATUREPOS[1], Dashboard.MARGIN)

        #Modus
        pygame.draw.rect(self.screen, Dashboard.MARGINCOLOR, self.modusarea, Dashboard.MARGIN)
        self.showText("MODUS", Dashboard.MODUSPOS[0], Dashboard.MODUSPOS[1], Dashboard.MARGIN)

        #BUTTONS
        #Button Freier Modus
        self.freiermodus.showButton(self.screen)
        #Button Ball folgen (Absolut)
        self.ballfolgenabsolut.showButton(self.screen)
        #Button Ball folgen (cm)
        self.ballfolgencm.showButton(self.screen)
        #Button Gesichtserkennung
        self.gesichtserkennung.showButton(self.screen)



        #Max Resolution
        pygame.draw.rect(self.screen, Dashboard.MARGINCOLOR, self.maxresolution)
        pygame.display.flip()

        return videostatus


class Button:

    MARGIN = 5
    MARGINCOLOR = (0, 0, 0)
    HOVERMARGINCOLOR = (100, 100, 100)
    PRESSEDMARGINCOLOR = (255, 0, 0)
    TEXTCOLOR = (0, 0, 0)
    TEXTBACKGROUNDCOLOR = (255, 255, 255)

    def __init__(self, text, x, y):
        FONT = pygame.font.SysFont("bahnschrift", 40, False, False)
        self.button = FONT.render(text, True, Button.TEXTCOLOR, self.TEXTBACKGROUNDCOLOR)
        buttonsize = pygame.font.Font.size(FONT, text)
        self.margin = pygame.Rect(x-Button.MARGIN, y-Button.MARGIN, buttonsize[0]+2*Button.MARGIN, buttonsize[1]+2*Button.MARGIN)
        self.pressed = False

    def showButton(self, screen):
        pygame.draw.rect(screen, self.MARGINCOLOR, self.margin)
        screen.blit(self.button, (self.margin.x+Button.MARGIN, self.margin.y+Button.MARGIN))

    def ispressed(self):
        mousepos = pygame.mouse.get_pos()
        mousepressed = pygame.mouse.get_pressed()[0]
        if self.margin.collidepoint(mousepos):
            #self.MARGINCOLOR = Button.HOVERMARGINCOLOR
            if mousepressed and not self.pressed:
                self.pressed = True
                return True
        #else:
            #self.MARGINCOLOR = Button.MARGINCOLOR
        if not mousepressed:
            self.pressed = False
        return False