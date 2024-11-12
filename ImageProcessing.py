#BILDVERARBEITUNG
#----------------------------------------------

import cv2
import pygame
from face_lib import face_lib

hsvmin = [180,255,255]
hsvmax = [0,0,0]

FL = face_lib()
def processImage(img, status):

    if status == 0: # Bei manuellem Betrieb

        finalimg = pygame.image.frombuffer(img.tostring(), img.shape[1::-1], "RGB")

        return finalimg,[0,1,0,0,0,0,0,0,0,0,0,0]  # Zweiter Wert ist Steuerungsmodus

    elif status == 5: # FARBCHECK, NUR FÜR FARBTESTS, UNVERWENDET

        img = cv2.GaussianBlur(img, (5, 5), 5)  # Bild blurren gegen Rauschen

        hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

        height, width = hsv_img.shape[:2]

        #Referenz-Rechteck in Bildmitte erzeugen
        start = (int(width / 2) - 5, int(height / 2) - 5)
        end = (int(width / 2) + 5, int(height / 2) + 5)
        color= (255, 0, 0)

        cv2.rectangle(img, start , end, color= color, thickness=2)

        #Aktuellen Farbwert des mittleren Pixels ermitteln
        hsvcur = hsv_img[int(height/2),int(width/2)]

        # Min- und Max-Werte aktualisieren
        if hsvcur[0] > hsvmax[0]:
            hsvmax[0] = hsvcur[0]
        if hsvcur[0] < hsvmin[0]:
            hsvmin[0] = hsvcur[0]
        if hsvcur[1] > hsvmax[1]:
            hsvmax[1] = hsvcur[1]
        if hsvcur[1] < hsvmin[1]:
            hsvmin[1] = hsvcur[1]
        if hsvcur[2] > hsvmax[2]:
            hsvmax[2] = hsvcur[2]
        if hsvcur[2] < hsvmin[2]:
            hsvmin[2] = hsvcur[2]

        cv2.putText(img, str(hsv_img[int(height/2),int(width/2)]), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,
                    cv2.LINE_AA)

        cv2.putText(img, "min: " + str(hsvmin), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255), 2,
                    cv2.LINE_AA)

        cv2.putText(img, "max: " + str(hsvmax), (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255), 2,
                    cv2.LINE_AA)

        cv2.imshow("test",img)

        finalimg = pygame.image.frombuffer(img.tostring(), img.shape[1::-1], "RGB")  # Formatierung für Pygame

        return finalimg, [0,1,0,0,0,0,0,0,0,0,0,0]  # Zweiter Wert ist Steuerungsmodus


    elif status == 1: # Ball folgen Absolut

        img = cv2.blur(img,(5,5)) #Bild blurren gegen Rauschen

        img, movex, movez, movenear = followBallAbsolute(img)

        finalimg = pygame.image.frombuffer(img.tostring(), img.shape[1::-1], "RGB")  # Formatierung für Pygame

        return finalimg, [1, 1, movez, 0, movenear, movex, 0, 0, 0, 0, 0, 0] # Zweiter Wert ist Steuerungsmodus

    elif status == 2:  # Ball Folgen CM

        img = cv2.blur(img, (5, 5))  # Bild blurren gegen Rauschen

        img, movex, movez, movenear = followBallCM(img)

        finalimg = pygame.image.frombuffer(img.tostring(), img.shape[1::-1], "RGB")  # Formatierung für Pygame

        return finalimg, [1, 2, movez, 0, movenear, movex, 0, 0, 0, 0, 0, 0]  # Zweiter Wert ist Steuerungsmodus


    elif status == 3: #GESICHTSERKENNUNG inkl Drehung

        img, rotation = RotateFace(img)

        finalimg = pygame.image.frombuffer(img.tostring(), img.shape[1::-1], "RGB")  # Formatierung für Pygame

        return finalimg, [1, 1, 0, rotation * 2, 0, 0, 0, 0, 0, 0, 0, 0]  # Zweiter Wert ist Steuerungsmodus


def followBallAbsolute(img): #BALL MIT ABSOLUTEN GESCHWINDIGKEITEN FOLGEN

    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    movex = 0
    movez = 0
    movenear = 0

    diffx, diffy, size, img = getBallPos(hsv_img, img) #Position des Balls

    diffx = -diffx  #Werte für Verarbeitung in diesem Modus invertieren
    diffy = -diffy

    # Skalierungswerte für seitliche Ball-Bewegung
    movemindiff = 30
    movemaxscalediff = 200
    movescalestart = 20
    movemaxspeed = 20

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

    # Skalierungswerte für Ball-Entfernung
    sizemiddle = 750
    sizemindiff = 40
    sizemaxscalediff = 200
    sizescalestart = 20
    sizemaxspeed = 10

    sizediff = size - sizemiddle

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
                "movex: " + str(round(movex)) + "; movez: " + str(round(movez)) + "; movenear: " + str(round(movenear)),
                (50, 700), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 0, 255), 2,
                cv2.LINE_AA)

    return img, round(movex), round(movez), round(movenear)


def followBallCM(img):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    height, width = img.shape[:2]

    diff_x_cm = 0
    diff_y_cm = 0
    movenear = 0

    diffx, diffy, size, img = getBallPos(hsv_img, img) #Position des Balls

    if (abs(diffx)+abs(diffy)) > 0:

        max_dist_x = (-0.021*size) + 65
        max_dist_y = max_dist_x * (height/width)

        movemindiff = 20

        diff_x_cm = -round((diffx / width) * max_dist_x)
        diff_y_cm = round((diffy / height) * max_dist_y)

        if abs(diff_x_cm) < movemindiff:
            diff_x_cm = 0
        if abs(diff_y_cm) < movemindiff:
            diff_y_cm = 0

        cv2.putText(img,
                    "[cm] x-diff: " + str(diff_x_cm) + "; z-diff: " + str(diff_y_cm),
                    (50, 700), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255), 2,
                    cv2.LINE_AA)

    return img, diff_x_cm,diff_y_cm,0

def RotateFace(img):
    rotation = 0

    no_of_faces, faces_coors = FL.faces_locations(img)

    if no_of_faces > 0:
        cv2.rectangle(img, faces_coors[0][0:2], (faces_coors[0][0] + faces_coors[0][2], faces_coors[0][1] + faces_coors[0][3]), (255, 0, 0), 2)  # Wahrscheinlich addition

        height, width = img.shape[:2]

        curx = faces_coors[0][0] + int(faces_coors[0][2]/2)
        cv2.circle(img, (curx,int(height/2)), 10, (255,0,0),2)
        diffx = (int(width / 2) - curx)

        rotation = -int(diffx/height * 65)

        cv2.putText(img,
                    "Rotation: " + str(rotation) + " deg",
                    (50, 700), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255), 2,
                    cv2.LINE_AA)

    if not(rotation > 5 or rotation < -5):
        rotation = 0

    return img, rotation

def getBallPos(hsv_img, img):

    diffx = 0
    diffy = 0
    size = 0

    lower = (35, 30, 40)  # fixHSVRange(135,20,20
    upper = (90, 255, 253)  # fixHSVRange(190,100,100)

    height, width = hsv_img.shape[:2]

    mask = cv2.inRange(hsv_img, lower, upper)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        if len(c) > 5 and c.size > 300:
            cv2.drawContours(hsv_img, c, -1, (0, 0, 255), 1)

            rct = cv2.fitEllipse(c)
            cv2.ellipse(img, rct, (0, 0, 255), 3)

            curx = int(rct[0][0])
            cury = int(rct[0][1])

            diffx = (int(width / 2) - curx)
            diffy = (int(height / 2) - cury)

            cv2.putText(img,
                        "[px] x: " + str(curx) + "; y: " + str(cury) + "; diffx: " + str(diffx) + "; diffy: " + str(diffy),
                        (50, 600), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 2,
                        cv2.LINE_AA)
            cv2.putText(img,
                        "Flaeche: " + str(c.size),
                        (50, 650), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 2,
                        cv2.LINE_AA)

            size = c.size

    return diffx, diffy, size, img

def fixHSVRange(h, s, v):
    # Normal H,S,V: (0-360,0-100%,0-100%)
    # OpenCV H,S,V: (0-180,0-255 ,0-255)
    return (180 * h / 360, 255 * s / 100, 255 * v / 100)