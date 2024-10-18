from djitellopy import tello
import pygame
import numpy

class dronecomms(object):
    
    def __init__(self):

        self.MYTELLO = tello.Tello()
        self.initialised = True

        self.tookoff = False
        self.moving = False
        self.connected = False

        self.takeoff_initiated = False
        
    def connect(self):
        self.MYTELLO.connect()
        try:

            self.connected = True
        except:
            print("Fehler connect")

    def getBattery(self):
        
        if self.connected:
            try:
                return self.MYTELLO.get_battery()
            except:
                print("Fehler bat")

    def streamon(self):
        if self.connected:
            try:
                self.MYTELLO.streamon()
            except:
                print("Fehler stream")

    def streamoff(self):
        if self.connected:
            try:
                self.MYTELLO.streamoff()
            except:
                print("Fehler streamo")

    def takeoff(self):

        if self.connected and self.tookoff == False:
            try:
                self.MYTELLO.takeoff()
                self.tookoff = True
            except:
                print("Fehler takeoff")
    def land(self):
        
        if self.connected and self.tookoff:
            try:
                self.MYTELLO.land()
                self.tookoff = False 
            except:
                print("Fehler lnd")
            
    def getspeed(self, dir):

        if self.connected:
            if dir == "x":
                return self.MYTELLO.get_speed_x()
            elif dir == "y":
                return self.MYTELLO.get_speed_y()
            else:
                return self.MYTELLO.get_speed_z()

    def getacceleration(self, dir):
        if self.connected:
            if dir== "x":
                return self.MYTELLO.get_acceleration_x()
            elif dir == "y":
                return self.MYTELLO.get_acceleration_y()
            else:
                return self.MYTELLO.get_acceleration_z()

    def getheight(self):
        if self.connected:
            try:
                return self.MYTELLO.get_height()
            except:
                print("Fehler")

    def gettemperature(self):
        if self.connected:
            try:
                return self.MYTELLO.get_temperature()
            except:
                print("Fehler tmp")



    def getImage(self):

        try:
            img = self.MYTELLO.get_frame_read().frame
            #img = pygame.image.frombuffer(img.tostring(), img.shape[1::-1],"RGB") # Formatierung
            return img
        
        except: 
            print("Fehler img")

    def flip(self):
        
        if self.tookoff:
            self.MYTELLO.flip_forward()

    def sendcontrols(self,mode, movementtable):

        # Steuerungsstandard: [Eingabe gegeben, Eingabemodus, Hoch + Runter, Drehen Uhrzeigersinn + Gegenuhrzeigersinn, Vorwärts + Rückwärts, Rechts + Links, starten + Landen, Manuell, Auto1, Auto2, Auto3]
        # [False oder True, 0 und 1, -100 bis 100, -100 bis 100, -100 bis 100, -100 bis 100, 0 und 1, 0 und 1, 0 und 1, 0 und 1, 0 und 1]

        if self.connected:
            if movementtable[4] == 1 and self.takeoff_initiated == False:
                self.takeoff_initiated = True
                if self.tookoff == False: # takeoff
                    self.takeoff()

                elif self.tookoff:       # land
                    self.MYTELLO.send_rc_control(0,0,0,0)
                    self.land()

            elif movementtable[4] == 0 and self.takeoff_initiated:
                self.takeoff_initiated = False

            if self.tookoff:
                if movementtable[5] == 1:   # optional flip
                    self.flip()
                if mode == 1: # move constantly
                    if abs(movementtable[0]) + abs(movementtable[1]) + abs(movementtable[2]) + abs(movementtable[3]) > 10:  # move drone
                        self.MYTELLO.send_rc_control(int(movementtable[3]), int(movementtable[2]), int(movementtable[0]), int(movementtable[1]))
                        self.moving = True
                        #print("sende")
                    elif abs(movementtable[0]) + abs(movementtable[1]) + abs(movementtable[2]) + abs(movementtable[3]) <= 10 and self.moving == True: # stop movement
                        self.MYTELLO.send_rc_control(0,0,0,0)
                        self.moving = False

                elif mode == 2: # move in cm's
                    if movementtable[0] > 0:
                        print("hoch")
                        self.MYTELLO.move_up(abs(movementtable[0]))
                    elif movementtable[0] < 0:
                        print("runter")
                        self.MYTELLO.move_down(abs(movementtable[0]))
                    if movementtable[1] > 0:
                        self.MYTELLO.rotate_clockwise(abs(movementtable[1]))
                    elif movementtable[1] < 0:
                        self.MYTELLO.rotate_counter_clockwise(abs(movementtable[1]))
                    if movementtable[2] > 0:
                        self.MYTELLO.move_forward(abs(movementtable[2]))
                    elif movementtable[2] < 0:
                        self.MYTELLO.move_back(abs(movementtable[2]))
                    if movementtable[3] > 0:
                        print("rechts")
                        self.MYTELLO.move_right(abs(movementtable[3]))
                    elif movementtable[3] < 0:
                        print("links")
                        self.MYTELLO.move_left(abs(movementtable[3]))
