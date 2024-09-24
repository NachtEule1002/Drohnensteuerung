from inputs import get_gamepad
import math
import threading

class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)
    
    def __init__(self):

        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.PadUD = 0
        self.PadLR = 0


        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()



    def read(self): # return the buttons/triggers that you care about in this methode
        xl = round(self.LeftJoystickX, 2)
        yl = round(self.LeftJoystickY, 2)
        xr = round(self.RightJoystickX, 2)
        yr = round(self.RightJoystickY, 2)
        a = round(self.A, 2)
        b = round(self.B, 2) # b=1, x=2
        x = round(self.X, 2)
        y = round(self.Y, 2)
        rb = round(self.RightBumper, 2)
        lb = round(self.LeftBumper, 2)
        padleftright = round(self.PadLR, 2)
        padupdown = round(self.PadUD, 2)

        # control-standard: [True or False, up + down, rotate cw + ccw, forward + backward, right + left, takeoff + land, flip, Button3 (unass.), Button4 (unass.)]
        # [-100 to 100, -100 to 100, -100 to 100, -100 to 100, 0 or 1, 0 or 1, 0 or 1, 0 or 1]


        if abs(xl)+abs(yl)+abs(xr)+abs(yr)+a+b+rb+lb+a+b+x+y+abs(padupdown)+abs(padleftright) > 0: # check, if something is pressed on the controller
            iscontrol = True
        else:
            iscontrol = False

        if padupdown == 1:
            padup = 0
            paddown = 1
        elif padupdown == -1:
            padup = 1
            paddown = 0
        else:
            padup = 0
            paddown = 0

        if padleftright == 1:
            padleft = 0
            padright = 1
        elif padleftright == -1:
            padleft = 1
            padright = 0
        else:
            padleft = 0
            padright = 0

        return [int(iscontrol), int(yr*100), int(xr*100), int(yl*100), int(xl*100), a, b, y, padup, padright, paddown, padleft]

        # A für Takeoff, B für Flip, X für Modus 1, Y für Modus 0

    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.Y = event.state #previously switched with X
                elif event.code == 'BTN_WEST':
                    self.X = event.state #previously switched with Y
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'ABS_HAT0Y':
                    self.PadUD = event.state
                elif event.code == 'ABS_HAT0X':
                    self.PadLR = event.state
