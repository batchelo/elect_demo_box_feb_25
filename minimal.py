#start_demo_box.py
import time
import board
# for the light strings
import neopixel
#for the MP3 player
import digitalio
from audiomp3 import MP3Decoder
from audiopwmio import PWMAudioOut as AudioOut
#for the servo motor
import pwmio
from adafruit_motor import servo
import digitalio
from digitalio import DigitalInOut, Direction, Pull
#for the temp/humidity sensor
import adafruit_dht
#for the ultrasound sensor
import adafruit_hcsr04
#for the liquid crystal display
import busio
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface
from lcd.lcd import CursorMode
#for the accelerometer
from adafruit_bus_device.i2c_device import I2CDevice 
import adafruit_lis3dh


#define some properties that will be used later

#regarding the lights
pixel_pin = board.GP22

# The number of NeoPixels
num_pixels = 52

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRBW

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER)

#regarding the LCD display
i2c_d = busio.I2C(scl=board.GP11, sda=board.GP10)
lcd = LCD(I2CPCF8574Interface(i2c_d, 0x27), num_rows=2, num_cols=16)
#lcd_d._backlight_pin_state = LCD_NOBACKLIGHT

#regarding the temp_humidity module
dhtDevice = adafruit_dht.DHT11(board.GP4) # specs for the temp/hum module

#regarding the accelerometer
i2c = busio.I2C(board.GP21, board.GP20)
device = I2CDevice(i2c, 0x18)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c)

# Set range of accelerometer (can be RANGE_2_G, RANGE_4_G, RANGE_8_G or RANGE_16_G).
lis3dh.range = adafruit_lis3dh.RANGE_2_G

#regarding the ultrasound sensor
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP19, echo_pin=board.GP18)

#regarding the servo
# create a PWMOut object on Pin GP3.
pwm = pwmio.PWMOut(board.GP3, duty_cycle=2 ** 15, frequency=50)
toggle = digitalio.DigitalInOut(board.GP6)
toggle.direction = digitalio.Direction.INPUT
toggle.pull = Pull.DOWN # the digitalio documentation says that the pulldown resistor is weak and useless
# therefore, I need to insert a "strong" external pull-down resistor.  They suggest 8.2 k oms or less.

# Create a servo object, my_servo.
my_servo = servo.Servo(pwm)
my_servo.angle = 85
#print (toggle.value)

#start the intro schema by playing the intro audio message
audio = AudioOut(board.GP17)
path = "sounds/"

filename = "weee.mp3" #instantiates the object
mp3_file = open(path + filename, "rb")
decoder = MP3Decoder(mp3_file)

def play_intro(filename):
    decoder.file = open(path + filename, "rb")
    audio.play(decoder)
    while audio.playing:
        pass
def play_lights(filename):
    decoder.file = open(path + filename, "rb")
    audio.play(decoder)
    while audio.playing:
        pass
def play_UM(filename):
    decoder.file = open(path + filename, "rb")
    audio.play(decoder)
    while audio.playing:
        pass
def play_hope(filename):
    decoder.file = open(path + filename, "rb")
    audio.play(decoder)
    while audio.playing:
        pass
play_intro("intro_l.mp3")
play_lights("lights.mp3")
play_UM("UM_respond.mp3")
play_hope("hope.mp3")
#go into POST-INTRO state: (1) display "Forge" text, (2) blink lights in a pattern, (3) monitor UM switch
while True:
    lcd.clear()
# Start at the second line, fifth column (numbering from zero).
    lcd.set_cursor_pos(0, 4)
    lcd.print("The Forge")
    lcd.set_cursor_pos(1,3)
    lcd.print("Makerspace")
# Make the cursor visible as a line.
#     lcd.set_cursor_mode(CursorMode.LINE)
#start light strips    
    def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos * 3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
        else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)
        return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

    def rainbow_cycle(wait):
        for j in range(255):
            for i in range(num_pixels):
                pixel_index = (i * 256 // num_pixels) + j
                pixels[i] = wheel(pixel_index & 255)
            pixels.show()
            time.sleep(wait)

    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill((255, 0, 0))
    pixels.show()
    time.sleep(1)
    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(1)
    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill((0, 0, 255))
    pixels.show()
    time.sleep(1)
    rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step
    
    if (toggle.value == True): #This pauses so long as GP6 is set to HIGH (3.3v); when it goes low, the servo rotates and returns
        angle = 10
        my_servo.angle = angle
        time.sleep(1)
        angle = 85
        my_servo.angle = angle
        time.sleep(1)

