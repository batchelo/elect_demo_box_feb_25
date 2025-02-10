import busio
import digitalio
import adafruit_lis3dh
import time
import board
import start_demo_box as sdb

mode_pin = digitalio.DigitalInOut(board.GP2)
i2c = busio.I2C(board.GP21, board.GP20)  # uses board.SCL and board.SDA
int1 = digitalio.DigitalInOut(board.GP9)  # Set this to the correct pin for the interrupt!
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)

# Set range of accelerometer (can be RANGE_2_G, RANGE_4_G, RANGE_8_G or RANGE_16_G).
lis3dh.range = adafruit_lis3dh.RANGE_2_G
if (mode_pin.value) == False:
    sdb.play_tilt("tap.mp3", 15)
    time.sleep(8)
    if lis3dh.tapped:
        print("Tapped!")
        decoder.file = open(path + "drum.mp3", "rb")
        audio.play(decoder)
        time.sleep(0.5)
    else:
        pass
    
else:
    sdb.demo_set2()
