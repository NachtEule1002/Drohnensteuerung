from djitellopy import tello
import cv2
import pygame
from PIL import Image
import dronecomms

pygame.init()
screen = pygame.display.set_mode((1500, 1000))
clock = pygame.time.Clock()
running = True

#tello = tello.Tello()
#tello.connect()
#tello.streamon()

drone = dronecomms.dronecomms()

#pfeil = pygame.image.load("pfeil.jpg")

while running:
# def imgtopygame(droneimg):
# Funktionsaufruf: Camera.imgtopy(drone.getImage())

#def imgtopygame(droneobj):
#Funktionsaufruf: Camera.imgtopy(drone)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    img = drone.getImage()
    #img = cv2.resize(img, (500,500))
    #img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    #cv2.imshow("Bild", img)
    #cv2.waitKey(1)
    
    #img = cv2.resize(img,(1920,1080))
    
    screen.blit(img, (0,0))


    pygame.display.flip()
    clock.tick(60)


pygame.quit()