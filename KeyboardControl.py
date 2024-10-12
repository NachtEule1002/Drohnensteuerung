# Tastatursteuerung

import pygame

def keyboardControl():

    # Tastenbelegung und -abfrage

    eingabe, ud, yv, fb, rl, start, flip, modaus, mod1, mod2, mod3, mod4 = False, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
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
    elif gedrueckt[pygame.K_f]:
        flip = 1
        eingabe = True
    if gedrueckt[pygame.K_1]:
        modaus = 1
        eingabe = True
    elif gedrueckt[pygame.K_2]:
        mod1 = 1
        eingabe = True
    elif gedrueckt[pygame.K_3]:
        mod2 = 1
        eingabe = True
    elif gedrueckt[pygame.K_4]:
        mod3 = 1
        eingabe = True
    elif gedrueckt[pygame.K_5]:
        mod4 = 1
        eingabe = True
    return [int(eingabe), 1, ud, yv, fb, rl, start, flip, modaus, mod1, mod2, mod3, mod4]
    
