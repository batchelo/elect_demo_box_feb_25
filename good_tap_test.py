import time
import board
import busio
import digitalio
import adafruit_lis3dh

i2c = busio.I2C(board.GP21, board.GP20)  # uses board.SCL and board.SDA
int1 = digitalio.DigitalInOut(board.GP9)  # Set this to the correct pin for the interrupt!
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)

# Set range of accelerometer (can be RANGE_2_G, RANGE_4_G, RANGE_8_G or RANGE_16_G).
lis3dh.range = adafruit_lis3dh.RANGE_2_G

# Set tap detection to double taps.  The first parameter is a value:
#  - 0 = Disable tap detection.
#  - 1 = Detect single taps.
#  - 2 = Detect double taps.

# The second parameter is the threshold and a higher value means less sensitive
# tap detection.  Note the threshold should be set based on the range above:
#  - 2G = 40-80 threshold
#  - 4G = 20-40 threshold
#  - 8G = 10-20 threshold
#  - 16G = 5-10 threshold
lis3dh.set_tap(2, 20)

# Loop forever printing if a double tap is detected.
while True:
#    x, y, z = [value / adafruit_lis3dh.STANDARD_GRAVITY for value in lis3dh.acceleration]
#    print("x = %0.3f G, y = %0.3f G, z = %0.3f G" % (x, y, z))
    time.sleep(.5)
    if lis3dh.tapped:
        print("Tapped!")
        time.sleep(0.5)