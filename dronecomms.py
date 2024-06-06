from djitellopy import tello

class dronecomms(object):
    MYTELLO = tello.Tello()

    initialised = False

    def initialise(self, telloobj):

        self.MYTELLO = telloobj
        self.initialised = True

    def land(self):
        initialised = True
        if initialised:
            self.MYTELLO.land()


    def takeoff(self):

        if self.initialised:
            self.MYTELLO.takeoff()

    def sendcontrols(self, movementtable):

        # Steuerungsstandard: [Hoch + Runter, Drehen Uhrzeigersinn + Gegenuhrzeigersinn, Vorwärts + Rückwärts, Rechts + Links, starten, landen, Button3, Button4]
        # [-100 bis 100, -100 bis 100, -100 bis 100, -100 bis 100, 0 und 1, 0 und 1, 0 und 1, 0 und 1]
        
        print(self.initialised)
        if self.initialised:
            if movementtable[6] == 1:
                print("Motor an")
                self.MYTELLO.turn_motor_on()
            else:
                print("Motor aus")
                self.MYTELLO.turn_motor_off()