import time
import board
import digitalio
import start_demo_box as sdb

mode_pin = digitalio.DigitalInOut(board.GP2)

if (mode_pin.value) == False:
    sdb.demo_set1()
else:
    sdb.demo_set2()



