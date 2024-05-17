from djitellopy import tello
import KeyboardControl as kc
from time import sleep
import os 


kc.init()
me = tello.Tello()
me.connect()
print(me.get_battery())

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    if kc.getKey("LEFT"): lr = -speed
    elif kc.getKey("RIGHT"): lr = speed

    if kc.getKey("UP"): fb = speed
    elif kc.getKey("DOWN"): fb = -speed

    if kc.getKey("w"): ud = speed
    elif kc.getKey("s"): ud = -speed

    if kc.getKey("a"): yv = speed
    elif kc.getKey("d"): yv = -speed

    if kc.getKey("q"): me.land()
    if kc.getKey("e"): me.takeoff()

    return [lr, fb, ud, yv]


#HAUPTSCHLEIFE

while True:
    #clear()
    #DOME
    vals = getKeyboardInput()

    me.send_rc_control(vals[0],vals[1],vals[2],vals[3])

    #TOBI

    sleep(0.01)


    