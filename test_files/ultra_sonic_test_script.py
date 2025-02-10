import board
from os import utime
import pwmio
import digitalio
from digitalio import DigitalInOut, Direction, Pull

trigger = digitalio.DigitalInOut(board.GP19)
trigger.direction = Direction.OUTPUT
echo = digitalio.DigitalInOut(board.GP18)
echo.direction = Direction.INPUT

def ultra():
   trigger.value = False 
   utime.sleep_us(2)
   trigger.value = True
   utime.sleep_us(5)
   trigger.value = False
   while echo.value() == 0:
       signaloff = utime.ticks_us()
   while echo.value() == 1:
       signalon = utime.ticks_us()
   timepassed = signalon - signaloff
   distance = (timepassed * 0.0343) / 2
   print("The distance from object is ",distance,"cm")
while True:
   ultra()
   utime.sleep(1)
