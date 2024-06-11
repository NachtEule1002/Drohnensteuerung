from djitellopy import tello
import pygame

class dronecomms(object):
    
    def __init__(self):

        self.MYTELLO = tello.Tello()
        self.initialised = True

        self.tookoff = False
        self.moving = False
        self.connected = False
        
    def connect(self):
        
        try:
            self.MYTELLO.connect()
            self.connected = True
        except:
            print("Fehler")

    def getBattery(self):
        
        if self.connected:
            try:
                return self.MYTELLO.get_battery()
            except:
                print("Fehler")

    def streamon(self):
        if self.connected:
            try:
                self.MYTELLO.streamon()
            except:
                print("Fehler")

    def streamoff(self):
        if self.connected:
            try:
                self.MYTELLO.streamoff()
            except:
                print("Fehler")

    def land(self):
        
        if self.connected and self.tookoff:
            try:
                self.MYTELLO.land()
                self.tookoff = False 
            except:
                print("Fehler")
            
    def getspeed(self, dir):

        if self.connected:
            if dir== "x":
                return self.MYTELLO.get_speed_x
            elif dir == "y":
                return self.MYTELLO.get_speed_y
            else:
                self.MYTELLO.get_speed_z

    def getacceleration(self, dir):
        if self.connected:
            if dir== "x":
                return self.MYTELLO.get_acceleration_x
            elif dir == "y":
                return self.MYTELLO.get_acceleration_y
            else:
                self.MYTELLO.get_acceleration_z

    def getheight(self):
        if self.connected:
            try:
                return self.MYTELLO.get_height()
            except:
                print("Fehler")

    def getcurrentstate(self):
        if self.connected:
            try:
                return self.MYTELLO.get_current_state()
            except:
                print("Fehler")

    def gettemperature(self):
        if self.connected:
            try:
                return self.MYTELLO.get_temperature()
            except:
                print("Fehler")

    def takeoff(self):

        if self.connected and self.tookoff == False:
            try:
                self.MYTELLO.takeoff()
                self.tookoff = True
            except:
                print("Fehler")

    def getImage(self):

        try:
            img = self.MYTELLO.get_frame_read().frame
            img = pygame.image.frombuffer(img.tostring(), img.shape[1::-1],"RGB") # Formatierung
            return img
        
        except: 
            print("Fehler")

    def sendcontrols(self, movementtable):

        # Steuerungsstandard: [Hoch + Runter, Drehen Uhrzeigersinn + Gegenuhrzeigersinn, Vorwärts + Rückwärts, Rechts + Links, starten, landen, Button3, Button4]
        # [-100 bis 100, -100 bis 100, -100 bis 100, -100 bis 100, 0 und 1, 0 und 1, 0 und 1, 0 und 1]
        
        if self.connected:
            if movementtable[4] == 1 and self.tookoff == False:
                self.takeoff()
                
            elif movementtable[4]  == 1 and self.tookoff:
                self.MYTELLO.send_rc_control(0,0,0,0)
                self.land()
                        
            
            if abs(movementtable[0]) + abs(movementtable[1]) + abs(movementtable[2]) + abs(movementtable[3]) > 10:
                self.MYTELLO.send_rc_control(int(movementtable[3]), int(movementtable[2]), int(movementtable[0]), int(movementtable[1]))
                self.moving = True
                #print("sende")
            elif abs(movementtable[0]) + abs(movementtable[1]) + abs(movementtable[2]) + abs(movementtable[3]) <= 10 and self.moving == True:
                self.MYTELLO.send_rc_control(0,0,0,0)
                self.moving = False