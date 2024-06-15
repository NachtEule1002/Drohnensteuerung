# Tastatursteuerung

import pygame

def keyboardControl():

    # Tastenbelegung und -abfrage

    eingabe, ud, yv, fb, rl, start, land = False, 0, 0, 0, 0, 0, 0
    gedrueckt = pygame.key.get_pressed()
    if gedrueckt[pygame.K_UP]:
        ud = 100
        eingabe = True
    elif gedrueckt[pygame.K_DOWN]:
        ud = -100
        eingabe = True
    if gedrueckt[pygame.K_RIGHT]:
        yv = 100
        eingabe = True
    elif gedrueckt[pygame.K_LEFT]:
        yv = -100
        eingabe = True
    if gedrueckt[pygame.K_w]:
        fb = 100
        eingabe = True
    elif gedrueckt[pygame.K_s]:
        fb = -100
        eingabe = True
    if gedrueckt[pygame.K_d]:
        rl = 100
        eingabe = True
    elif gedrueckt[pygame.K_a]:
        rl = -100
        eingabe = True
    if gedrueckt[pygame.K_e]:
        start = 1
        eingabe = True
    elif gedrueckt[pygame.K_q]:
        land = 1
        eingabe = True
    return[eingabe, ud, yv, fb, rl, start, land, 0, 0]
    
