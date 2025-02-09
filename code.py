import time
import board
import digitalio
import start_demo_box as sdb
#for the Elon box, the line above is "start_demo_box_Elon as sdb"
#also, in the start_demo_box code, the hex address for the ultrasound device is 0x23 vs 0x27

mode_pin = digitalio.DigitalInOut(board.GP2)

if (mode_pin.value) == False:
    sdb.demo_set1()
else:
    sdb.demo_set2()



