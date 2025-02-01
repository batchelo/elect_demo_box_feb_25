"""CircuitPython Essentials Servo standard servo example"""
import time
import board
import pwmio
from adafruit_motor import servo
import digitalio
from digitalio import DigitalInOut, Direction, Pull

# create a PWMOut object on Pin GP3.
pwm = pwmio.PWMOut(board.GP3, duty_cycle=2 ** 15, frequency=50)
toggle = digitalio.DigitalInOut(board.GP6)
toggle.direction = digitalio.Direction.INPUT
toggle.pull = Pull.DOWN # the digitalio documentation says that the pulldown resistor is weak and useless
# therefore, I need to insert a "strong" external pull-down resistor.  They suggest 8.2 k oms or less.

# Create a servo object, my_servo.
my_servo = servo.Servo(pwm)
print (toggle.value)

my_servo.angle = 85
while True:
    if (toggle.value == True): #This pauses so long as GP6 is set to HIGH (3.3v); when it goes low, the servo rotates and returns
        angle = 10
        my_servo.angle = angle
        time.sleep(1)
        angle = 85
        my_servo.angle = angle
        time.sleep(1)
    else:
        pass
