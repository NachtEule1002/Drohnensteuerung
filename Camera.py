from djitellopy import tello
import cv2

tello = tello.Tello()
tello.connect()
tello.streamon()

print(tello.get_battery())

tello.turn_motor_on()

while True:
    img = tello.get_frame_read().frame
    img = cv2.resize(img, (500,500))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow("Bild", img)
    cv2.waitKey(1)
