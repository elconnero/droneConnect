from djitellopy import tello
import time

me = tello.Tello()
me.connect()
print("Ning Test: Battery Status")
print(me.get_battery())