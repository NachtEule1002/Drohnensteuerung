from djitellopy import tello

class dronecomms(object):
    
    initialised = False

    def __init__(self, telloobj):

        self.MYTELLO = telloobj
        self.initialised = True

        self.tookoff = False
        self.moving = False
        

    def land(self):
        initialised = True
        if initialised:
            try:
                self.MYTELLO.land()
                self.tookoff = False 
            except:
                print("nope")
            


    def takeoff(self):

        if self.initialised:
            try:
                self.MYTELLO.takeoff()
                self.tookoff = True
            except:
                print("nope")

    def sendcontrols(self, movementtable):

        # Steuerungsstandard: [Hoch + Runter, Drehen Uhrzeigersinn + Gegenuhrzeigersinn, Vorwärts + Rückwärts, Rechts + Links, starten, landen, Button3, Button4]
        # [-100 bis 100, -100 bis 100, -100 bis 100, -100 bis 100, 0 und 1, 0 und 1, 0 und 1, 0 und 1]
        
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