# Tastatursteuerung

import pygame
from djitellopy import tello

speed = 80

def keyboardControl():

    # Tastenbelegung und -abfrage

    rl, fb, ud, yv = 0, 0, 0, 0
    gedrueckt = pygame.key.get_pressed()
    if gedrueckt[pygame.K_UP]:
        fb = speed
    elif gedrueckt[pygame.K_DOWN]:
        fb = -speed
    if gedrueckt[pygame.K_RIGHT]:
        rl = speed        
    elif gedrueckt[pygame.K_LEFT]:
        rl = -speed
    if gedrueckt[pygame.K_w]:
        ud = speed
    elif gedrueckt[pygame.K_s]:
        ud = -speed
    if gedrueckt[pygame.K_d]:
        yv = speed
    elif gedrueckt[pygame.K_a]:
        yv = -speed
    if gedrueckt[pygame.K_e]:
        tello.takeoff()
    elif gedrueckt[pygame.K_q]:
        tello.land()
    tello.send_rc_control(rl, fb, ud, yv)
