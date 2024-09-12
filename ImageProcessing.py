#BILDVERARBEITUNG
#----------------------------------------------

import cv2
from PIL import Image
import numpy
import pygame

def processImage(img, status):

    #finalimg = img

    if status == 0:

        finalimg = pygame.image.frombuffer(img.tostring(), img.shape[1::-1], "RGB")

        return finalimg,[0,1,0,0,0,0,0,0,0,0]  # Zweiter Wert ist Steuerungsmodus

    elif status == 1:

        img = cv2.blur(img, (5, 5))  # Bild blurren gegen Rauschen

        img, movex, movez, movenear = followBallCM(img)

        finalimg = pygame.image.frombuffer(img.tostring(), img.shape[1::-1], "RGB")  # Formatierung für Pygame

        return finalimg, [1, 1, movez, 0, movenear, movex, 0, 0, 0, 0]  # Zweiter Wert ist Steuerungsmodus

    elif status == 2: #CURRENTLY DISABLED

        img = cv2.blur(img,(5,5)) #Bild blurren gegen Rauschen

        img, movex, movez, movenear = followBallAbsolute(img)

        finalimg = pygame.image.frombuffer(img.tostring(), img.shape[1::-1], "RGB")  # Formatierung für Pygame

        return finalimg, [1, 1, movez, 0, movenear, movex, 0,0, 0, 0] # Zweiter Wert ist Steuerungsmodus



def followBallAbsolute(img):

    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    lower = fixHSVRange(135,20,20)
    upper = fixHSVRange(190,230,230)

    mask = cv2.inRange(hsv_img,lower, upper)

    contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    movex = 0
    movez = 0
    movenear = 0

    if len(contours) > 0:
        c = max(contours,key = cv2.contourArea)
        if len(c) > 5 and c.size > 400:
            cv2.drawContours(img,c,-1,(0,0,255),1)

            #M = cv2.moments(c)

            #x = int(M["m10"]/(M["m00"]+0.01))
            #y = int(M["m01"]/(M["m00"]+0.01))

            #cv2.putText(img,"x: " + str(x) + "; y: " + str(y),(50,50),cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2,cv2.LINE_AA)

            rct = cv2.fitEllipse(c)
            cv2.ellipse(img,rct,(0,0,255),3)

            curx = int(rct[0][0])
            cury = int(rct[0][1])

            cv2.putText(img, "x: " + str(curx) + "; y: " + str(cury), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,
                        cv2.LINE_AA)

            diffx = -(int(img.shape[1] / 2) - curx)
            diffy = -(int(img.shape[0] / 2) - cury)

            cv2.putText(img, "x: " + str(curx) + "; y: " + str(cury) + "; diffx: "+ str(diffx) + "; diffy: " + str(diffy), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 2,
                        cv2.LINE_AA)
            cv2.putText(img,
                        "Flaeche: " + str(c.size),
                        (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 2,
                        cv2.LINE_AA)

            movemindiff = 30
            movemaxscalediff = 200
            movescalestart = 20
            movemaxspeed = 30

            if diffx > movemindiff:

                if diffx < movemaxscalediff:
                    movex = (movemaxspeed/(movemaxscalediff - movescalestart)) * diffx - movescalestart*(movemaxspeed/(movemaxscalediff - movescalestart))
                else:
                    movex = movemaxspeed

            elif diffx < -movemindiff:
                if abs(diffx) < movemaxscalediff:
                    movex = -((movemaxspeed / (movemaxscalediff - movescalestart)) * abs(diffx) - movescalestart * (movemaxspeed / (movemaxscalediff - movescalestart)))
                else:
                    movex = -movemaxspeed

            if diffy > movemindiff:
                if diffy < movemaxscalediff:
                    movez = -(movemaxspeed / (movemaxscalediff - movescalestart)) * diffy - movescalestart * (
                                movemaxspeed / (movemaxscalediff - movescalestart))
                else:
                    movez = -movemaxspeed

            elif diffy < -movemindiff:
                if abs(diffy) < movemaxscalediff:
                    movez = ((movemaxspeed / (movemaxscalediff - movescalestart)) * abs(diffy) - movescalestart * (
                                movemaxspeed / (movemaxscalediff - movescalestart)))
                else:
                    movez = movemaxspeed

            sizemiddle = 750
            sizemindiff = 40
            sizemaxscalediff = 200
            sizescalestart = 20
            sizemaxspeed = 40

            sizediff = c.size - sizemiddle

            if sizediff > sizemindiff:
                if sizediff < sizemaxscalediff:
                    movenear = -(sizemaxspeed / (sizemaxscalediff - sizescalestart)) * sizediff - sizescalestart * (
                                sizemaxspeed / (sizemaxscalediff - sizescalestart))
                else:
                    movenear = -sizemaxspeed

            elif sizediff < sizemindiff:
                if abs(sizediff) < sizemaxscalediff:
                    movenear = ((sizemaxspeed / (sizemaxscalediff - sizescalestart)) * abs(sizediff) - sizescalestart * (
                                sizemaxspeed / (sizemaxscalediff - sizescalestart)))
                else:
                    movenear = sizemaxspeed

            cv2.putText(img,
                        "movex: " + str(movex) + "; movez: " + str(movez) + ";movenear: " + str(movenear),
                        (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 2,
                        cv2.LINE_AA)


    cv2.imshow("Red",img)

    return (img, movex, movez, movenear)

def followBallCM(img):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    lower = fixHSVRange(135, 20, 20)
    upper = fixHSVRange(190, 230, 230)

    mask = cv2.inRange(hsv_img, lower, upper)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    movex = 0
    movez = 0
    movenear = 0

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        if len(c) > 5 and c.size > 400:
            cv2.drawContours(img, c, -1, (0, 0, 255), 1)

            rct = cv2.fitEllipse(c)
            cv2.ellipse(img, rct, (0, 0, 255), 3)

            curx = int(rct[0][0])
            cury = int(rct[0][1])

            cv2.putText(img, "x: " + str(curx) + "; y: " + str(cury), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 2,
                        cv2.LINE_AA)

            diffx = -(int(img.shape[1] / 2) - curx)
            diffy = -(int(img.shape[0] / 2) - cury)

            cv2.putText(img,
                        "x: " + str(curx) + "; y: " + str(cury) + "; diffx: " + str(diffx) + "; diffy: " + str(diffy),
                        (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 2,
                        cv2.LINE_AA)
            cv2.putText(img, "Flaeche: " + str(c.size),
                        (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 2,
                        cv2.LINE_AA)

            size = c.size

            # HIER NOCH BEWEGUNG EINFÜGEN



def fixHSVRange(h, s, v):
    # Normal H,S,V: (0-360,0-100%,0-100%)
    # OpenCV H,S,V: (0-180,0-255 ,0-255)
    return (180 * h / 360, 255 * s / 100, 255 * v / 100)