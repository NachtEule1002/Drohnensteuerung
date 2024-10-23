# DASHBOARD
#---------------------------------------------------

import pygame
import sys


class Dashboard:

    WINDOWWIDTH = 1910
    WINDOWHEIGHT = 905
    TEXTSIZE = 30
    TEXTCOLOR = (0, 0, 0)
    TEXTBACKGROUNDCOLOR = (255, 255, 255)
    MARGINCOLOR = (0, 0, 0)
    BACKGROUNDCOLOR = (115, 179, 189)
    MARGIN = 5
    VERTICALELEMENTDISTANCE = 50
    HORIZONTALDISTANCE = 20

    #Drohne nicht verbunden
    NODRONEPOS = 100 , 100


    #Camera
    CAMERAPOS = 10, 10
    CAMERAAREA = 960, 720

    #STATUS
    STATUSPOS = 1000, 10
    STATUSAREA = 333, 345

    #Battery
    BATTERYPOS = STATUSPOS[0] + HORIZONTALDISTANCE, STATUSPOS[1] + VERTICALELEMENTDISTANCE

    #Height
    HEIGHTPOS = STATUSPOS[0] + HORIZONTALDISTANCE, STATUSPOS[1] + 2 * VERTICALELEMENTDISTANCE

    #Temperature
    TEMPERATUREPOS = STATUSPOS[0] + HORIZONTALDISTANCE, STATUSPOS[1] + 3 * VERTICALELEMENTDISTANCE

    #Speed
    SPEEDXPOS = STATUSPOS[0] + HORIZONTALDISTANCE, STATUSPOS[1] + 4 * VERTICALELEMENTDISTANCE
    SPEEDYPOS = STATUSPOS[0] + HORIZONTALDISTANCE, STATUSPOS[1] + 5 * VERTICALELEMENTDISTANCE
    SPEEDZPOS = STATUSPOS[0] + HORIZONTALDISTANCE, STATUSPOS[1] + 6 * VERTICALELEMENTDISTANCE

    #MODUS
    MODUSPOS = 1000, 390
    MODUSAREA = 333, 245

    #Control
    CONTROLPOS = 1000, 670
    CONTROLAREA = 333, 153

    #Keyboard
    KEYBOARDPOS = 1360, 10

    #BUTTONS
    #Button Freier Modus
    FREIERMODUSPOS = MODUSPOS[0] + HORIZONTALDISTANCE, MODUSPOS[1] + VERTICALELEMENTDISTANCE
    #Button Ball folgen (Absolut)
    BALLFOLGENABSOLUTPOS = MODUSPOS[0] + HORIZONTALDISTANCE, MODUSPOS[1] + 2 * VERTICALELEMENTDISTANCE
    #Button Ball folgen (cm)
    BALLVERFOLGENCMPOS = MODUSPOS[0] + HORIZONTALDISTANCE, MODUSPOS[1] + 3 * VERTICALELEMENTDISTANCE
    #Button Gesichtserkennung
    GESICHTSERKENNUNGPOS = MODUSPOS[0] + HORIZONTALDISTANCE, MODUSPOS[1] + 4 * VERTICALELEMENTDISTANCE
    # Button Starten/Landen
    STARTENLANDENPOS = CONTROLPOS[0] + HORIZONTALDISTANCE, CONTROLPOS[1] + VERTICALELEMENTDISTANCE
    #Button Flip
    FLIPPOS = CONTROLPOS[0] + HORIZONTALDISTANCE, CONTROLPOS[1] + 2 * VERTICALELEMENTDISTANCE




    # Fenster erstellen und starten
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Dashboard.WINDOWWIDTH-10, Dashboard.WINDOWHEIGHT-70))
        pygame.display.set_caption("Dashboard Drohnensteuerung")
        self.FONT = pygame.font.SysFont("bahnschrift", Dashboard.TEXTSIZE, False, False)
        self.tastenbelegung = pygame.image.load("Tastenbelegung.png")

        #EXTRA AREAS
        #Status
        self.statusarea = pygame.Rect(Dashboard.STATUSPOS[0]-Dashboard.MARGIN, Dashboard.STATUSPOS[1]-Dashboard.MARGIN, Dashboard.STATUSAREA[0]+2*Dashboard.MARGIN, Dashboard.STATUSAREA[1]+2*Dashboard.MARGIN)

        #Modus
        self.modusarea = pygame.Rect(Dashboard.MODUSPOS[0]-Dashboard.MARGIN, Dashboard.MODUSPOS[1]-Dashboard.MARGIN, Dashboard.MODUSAREA[0]+2*Dashboard.MARGIN, Dashboard.MODUSAREA[1]+2*Dashboard.MARGIN)

        #Control
        self.controlarea = pygame.Rect(Dashboard.CONTROLPOS[0]-Dashboard.MARGIN, Dashboard.CONTROLPOS[1]-Dashboard.MARGIN, Dashboard.CONTROLAREA[0]+2*Dashboard.MARGIN, Dashboard.CONTROLAREA[1]+2*Dashboard.MARGIN)


        #BUTTONS
        #Button Freier Modus
        self.freiermodus = Button("Freier Modus", Dashboard.FREIERMODUSPOS[0], Dashboard.FREIERMODUSPOS[1])
        #Button Ball folgen (Absolut)
        self.ballfolgenabsolut = Button("Ball folgen (Absolut)", Dashboard.BALLFOLGENABSOLUTPOS[0], Dashboard.BALLFOLGENABSOLUTPOS[1])
        #Button Ball folgen (cm)
        self.ballfolgencm = Button("Ball folgen (cm)", Dashboard.BALLVERFOLGENCMPOS[0], Dashboard.BALLVERFOLGENCMPOS[1])
        #Button Gesichtserkennung
        self.gesichtserkennung = Button("Gesichtserkennung", Dashboard.GESICHTSERKENNUNGPOS[0], Dashboard.GESICHTSERKENNUNGPOS[1])
        #Button Flip
        self.flip = Button("Flip nach vorne", Dashboard.FLIPPOS[0], Dashboard.FLIPPOS[1])
        #Button Sarten/Landen
        self.startenlanden = Button("Starten - Landen", Dashboard.STARTENLANDENPOS[0], Dashboard.STARTENLANDENPOS[1])

    def checkForExit(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def showText(self, text, x, y, margin):
        img = self.FONT.render(text, True, Dashboard.TEXTCOLOR, Dashboard.TEXTBACKGROUNDCOLOR)
        imgsize = pygame.font.Font.size(self.FONT, text)
        margin = pygame.Rect(x-margin, y-margin, imgsize[0]+2*margin, imgsize[1]+2*margin)
        pygame.draw.rect(self.screen, Dashboard.MARGINCOLOR, margin)
        self.screen.blit(img, (x, y))

    def showPicture(self, img, x, y, margin):
        imgwidth = img.get_rect()[2]
        imgheight = img.get_rect()[3]
        margin = pygame.Rect(x-margin, y-margin, imgwidth+2*margin, imgheight+2*margin)
        pygame.draw.rect(self.screen, Dashboard.MARGINCOLOR, margin)
        self.screen.blit(img, (x, y))

    def checkButton(self, modus):

        eingabe, ud, yv, fb, rl, start, flip, freiermodus, ballfolgenabsolut, ballfolgencm, gesichtserkennung, mod4 = False, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

        if self.freiermodus.isPressed():
            modus = 0
            eingabe = True
        elif self.ballfolgenabsolut.isPressed():
            modus = 1
            eingabe = True
        elif self.ballfolgencm.isPressed():
            modus = 2
            eingabe = True
        elif self.gesichtserkennung.isPressed():
            modus = 3
            eingabe = True
        elif self.startenlanden.isPressed():
            start = 1
            eingabe = True
        elif self.flip.isPressed():
            flip = 1
            eingabe = True

        if modus == 0:
            self.freiermodus.MARGINCOLOR = Button.PRESSEDMARGINCOLOR
            freiermodus = 1
        else:
            self.freiermodus.MARGINCOLOR = Button.MARGINCOLOR
        if modus == 1:
            self.ballfolgenabsolut.MARGINCOLOR = Button.PRESSEDMARGINCOLOR
            ballfolgenabsolut = 1
        else:
            self.ballfolgenabsolut.MARGINCOLOR = Button.MARGINCOLOR
        if modus == 2:
            self.ballfolgencm.MARGINCOLOR = Button.PRESSEDMARGINCOLOR
            ballfolgencm = 1
        else:
            self.ballfolgencm.MARGINCOLOR = Button.MARGINCOLOR
        if modus == 3:
            self.gesichtserkennung.MARGINCOLOR = Button.PRESSEDMARGINCOLOR
            gesichtserkennung = 1
        else:
            self.gesichtserkennung.MARGINCOLOR = Button.MARGINCOLOR

        return [int(eingabe), 1, ud, yv, fb, rl, start, flip, freiermodus, ballfolgenabsolut, ballfolgencm, gesichtserkennung, mod4]

    def loadAll(self, img, height, battery, temperature, speedx, speedy, speedz,  modus):
        self.screen.fill(Dashboard.BACKGROUNDCOLOR)
        Dashboard.checkForExit(self)
        DashboardDaten = Dashboard.checkButton(self, modus)

        #GRAPHICS
        #Camera
        self.showPicture(img, Dashboard.CAMERAPOS[0], Dashboard.CAMERAPOS[1], Dashboard.MARGIN)
        self.showText("KAMERABILD", Dashboard.CAMERAPOS[0], Dashboard.CAMERAPOS[1], Dashboard.MARGIN)

        #Status
        pygame.draw.rect(self.screen, Dashboard.MARGINCOLOR, self.statusarea, Dashboard.MARGIN)
        self.showText("STATUS", Dashboard.STATUSPOS[0], Dashboard.STATUSPOS[1], Dashboard.MARGIN)

        #Battery
        self.showText("Batterie: " + str(battery) + " %", Dashboard.BATTERYPOS[0], Dashboard.BATTERYPOS[1], Dashboard.MARGIN)

        #Height
        self.showText("Höhe: " + str(height) + " cm", Dashboard.HEIGHTPOS[0], Dashboard.HEIGHTPOS[1], Dashboard.MARGIN)

        #Temperature
        self.showText("Temperatur: " + str(temperature) + " °C", Dashboard.TEMPERATUREPOS[0], Dashboard.TEMPERATUREPOS[1], Dashboard.MARGIN)

        #Speed
        self.showText("Geschw. X: " + str(speedx), Dashboard.SPEEDXPOS[0], Dashboard.SPEEDXPOS[1], Dashboard.MARGIN)
        self.showText("Geschw. Y: " + str(speedy), Dashboard.SPEEDYPOS[0], Dashboard.SPEEDYPOS[1], Dashboard.MARGIN)
        self.showText("Geschw. Z: " + str(speedz), Dashboard.SPEEDZPOS[0], Dashboard.SPEEDZPOS[1], Dashboard.MARGIN)

        #Modus
        pygame.draw.rect(self.screen, Dashboard.MARGINCOLOR, self.modusarea, Dashboard.MARGIN)
        self.showText("MODUS", Dashboard.MODUSPOS[0], Dashboard.MODUSPOS[1], Dashboard.MARGIN)

        #Control
        pygame.draw.rect(self.screen, Dashboard.MARGINCOLOR, self.controlarea, Dashboard.MARGIN)
        self.showText("STEUERUNG", Dashboard.CONTROLPOS[0], Dashboard.CONTROLPOS[1], Dashboard.MARGIN)

        #BUTTONS
        #Button Freier Modus
        self.freiermodus.showButton(self.screen)
        #Button Ball folgen (Absolut)
        self.ballfolgenabsolut.showButton(self.screen)
        #Button Ball folgen (cm)
        self.ballfolgencm.showButton(self.screen)
        #Button Gesichtserkennung
        self.gesichtserkennung.showButton(self.screen)
        #Button Flip
        self.flip.showButton(self.screen)
        #Button Flip
        self.startenlanden.showButton(self.screen)

        #Tastenbelegung
        self.showPicture(self.tastenbelegung, Dashboard.KEYBOARDPOS[0], Dashboard.KEYBOARDPOS[1], Dashboard.MARGIN)

        pygame.display.flip()

        return DashboardDaten

    def loadNotConnected(self):
        Dashboard.checkForExit(self)
        self.screen.fill(Dashboard.BACKGROUNDCOLOR)
        self.showText("Drohne nicht verbunden!!!", Dashboard.NODRONEPOS[0], Dashboard.NODRONEPOS[1], Dashboard.MARGIN)
        pygame.display.flip()


class Button:

    MARGIN = 5
    MARGINCOLOR = (0, 0, 0)
    HOVERMARGINCOLOR = (100, 100, 100)
    PRESSEDMARGINCOLOR = (255, 0, 0)
    TEXTCOLOR = (0, 0, 0)
    TEXTBACKGROUNDCOLOR = (255, 255, 255)

    def __init__(self, text, x, y):
        FONT = pygame.font.SysFont("bahnschrift", Dashboard.TEXTSIZE, False, False)
        self.button = FONT.render(text, True, Button.TEXTCOLOR, self.TEXTBACKGROUNDCOLOR)
        buttonsize = pygame.font.Font.size(FONT, text)
        self.margin = pygame.Rect(x-Button.MARGIN, y-Button.MARGIN, buttonsize[0]+2*Button.MARGIN, buttonsize[1]+2*Button.MARGIN)
        self.pressed = False

    def showButton(self, screen):
        pygame.draw.rect(screen, self.MARGINCOLOR, self.margin)
        screen.blit(self.button, (self.margin.x+Button.MARGIN, self.margin.y+Button.MARGIN))

    def isPressed(self):
        mousepos = pygame.mouse.get_pos()
        mousepressed = pygame.mouse.get_pressed()[0]
        if self.margin.collidepoint(mousepos):
            if mousepressed and not self.pressed:
                self.pressed = True
                return True
        if not mousepressed:
            self.pressed = False
        return False