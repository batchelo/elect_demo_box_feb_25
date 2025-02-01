#For The Forge
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
num_pixels = 54

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
#ORDER = neopixel.GRBW

#pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER)

#regarding the LCD display
i2c_d = busio.I2C(scl=board.GP11, sda=board.GP10)
lcd = LCD(I2CPCF8574Interface(i2c_d, 0x23), num_rows=2, num_cols=16)
#lcd_d._backlight_pin_state = LCD_NOBACKLIGHT

#regarding the temp_humidity module
dhtDevice = adafruit_dht.DHT11(board.GP4) # specs for the temp/hum module

#regarding the accelerometer
i2c = busio.I2C(board.GP21, board.GP20)
device = I2CDevice(i2c, 0x18)
int1 = digitalio.DigitalInOut(board.GP9)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)

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
    
def play_sounds(filename):
    decoder.file = open(path + filename, "rb")
    audio.play(decoder)
    while audio.playing:
        pass

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
    # return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)
    return (r, g, b, 0)

def rainbow_cycle(pixels, wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
    pixels.show()
    time.sleep(wait)

def play_lights(filename, count):
    if filename == None:
        pass
    else:
        decoder.file = open(path + filename, "rb")
        audio.play(decoder)
        
    ORDER = neopixel.GRBW
    with neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER) as pixels:
        for i in range(count):
            # Comment this line out if you have RGBW/GRBW NeoPixels
            pixels.fill((255, 0, 0))
            pixels.show()
            time.sleep(0.1)
            # Comment this line out if you have RGBW/GRBW NeoPixels
            pixels.fill((0, 255, 0))
            pixels.show()
            time.sleep(0.1)
            # Comment this line out if you have RGBW/GRBW NeoPixels
            pixels.fill((0, 0, 255))
            pixels.show()
            time.sleep(0.1)
            #rainbow_cycle(pixels, 0.001)  # rainbow cycle with 1ms delay per step

        pixels.fill((0, 0, 0))
        pixels.show()
    # needed for persistance before next demo
    time.sleep(2)


def play_display(filename, seconds):

    lcd.clear()
    # Start at the second line, fifth column (numbering from zero).
    lcd.set_cursor_pos(0, 4)
    lcd.print("The Forge")
    lcd.set_cursor_pos(1,0)
    lcd.print("Makerspace")
    ####
    if filename == None:
        pass
    else:
        decoder.file = open(path + filename, "rb")
        audio.play(decoder)
    ####
    # needed for persistance before next demo
    time.sleep(seconds)

        
def play_temp(filename, seconds):
    state = False
    decoder.file = open(path + filename, "rb")
    try:
        # Print the values to the display
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        lcd.clear()
        # Start at the second line, fifth column (numbering from zero).
        lcd.set_cursor_pos(0, 0)
        lcd.print("Temp is: "+str(temperature_f))
        lcd.set_cursor_pos(1,0)
        lcd.print("Humidity is: "+str(humidity))
        state = True
        time.sleep(0.5)
    except:
        dhtDevice.exit()
        
    if state:
        audio.play(decoder)
    # needed for persistance before next demo
    time.sleep(seconds)
                
def play_tilt(filename, duration):
    decoder.file = open(path + filename, "rb")
    audio.play(decoder)
    for i in range(duration):
        # Read accelerometer values (in m / s ^ 2).  Returns a 3-tuple of x, y,
        # z axis values.  Divide them by 9.806 to convert to Gs.
         x, y, z = [value / adafruit_lis3dh.STANDARD_GRAVITY for value in lis3dh.acceleration]
         lcd.clear()
         lcd.set_cursor_pos(0, 0)
         lcd.print("x&y: "+str(x)+" "+str(y))
         lcd.set_cursor_pos(1,0)
         lcd.print("z: "+str(z))
        #Small delay to keep things responsive but give time for interrupt processing.
         time.sleep(0.5)
    # needed for persistance before next demo
    time.sleep(.5)
    lcd.clear()
    # Start at the second line, fifth column (numbering from zero).
    lcd.set_cursor_pos(0, 4)
    lcd.print("The Forge")
    lcd.set_cursor_pos(1,0)
    lcd.print("Makerspace")
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
    for i in range(duration):
        time.sleep(2)
        if lis3dh.tapped:
            print("Tapped!")
            decoder.file = open(path + "drum.mp3", "rb")
            audio.play(decoder)
            while audio.playing:
                pass
            time.sleep(.5)
            decoder.file = open(path + "again.mp3", "rb")
            audio.play(decoder)
            time.sleep(.5)
'''            for i in range(duration):
                if lis3dh.tapped:
                    print("Tapped second time!")
                    decoder.file = open(path + "vlad.mp3", "rb")
                    audio.play(decoder)
                    while audio.playing:
                        pass 
''' 
def color_all(pixels, color):
    pl = len(pixels)
    print('pixels length', pl)
    for i in range(pl):
        pixels[i] = color
        
def play_distance(filename, duration):
    decoder.file = open(path + filename, "rb")
    audio.play(decoder)

    #ORDER = neopixel.GRBW
    with neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False) as pixels:
        pixels.fill((255, 255, 255))
        for i in range(duration):
            try:
                dist = sonar.distance
            except RuntimeError:
                dist = 50 # so it display white until it registers
                print("Retrying!")
            print('distance', i, dist)
            if dist > 40:
                lcd.clear()
                lcd.set_cursor_pos(0, 0)
                sd = f'dist:40+'
                lcd.print("Dis = "+sd)
                lcd.set_cursor_pos(1,0)
                lcd.print("color = white")
                #color_all(pixels, (255, 0, 0))
                pixels.fill((255, 255, 255))
                pixels.show()
            if dist > 30 and dist < 40:
                lcd.clear()
                lcd.set_cursor_pos(0, 0)
                sd = f'dist:30-40'
                lcd.print("Dis = "+sd)
                lcd.set_cursor_pos(1,0)
                lcd.print("color = blue")
                #color_all(pixels, (0, 255, 0))
                pixels.fill((0, 0, 255))
                pixels.show()
            if dist > 20 and dist < 30:
                lcd.clear()
                lcd.set_cursor_pos(0, 0)
                sd = f'dist:20-30'
                lcd.print("Dis = "+sd)
                lcd.set_cursor_pos(1,0)
                lcd.print("color = green")
                #color_all(pixels, (0, 0, 255))
                pixels.fill((0, 255, 0))
                pixels.show()
            if dist < 20:
                lcd.clear()
                lcd.set_cursor_pos(0, 0)
                sd = f'dist:20-'
                lcd.print("Dis = "+sd)
                lcd.set_cursor_pos(1,0)
                lcd.print("color = red")
                #color_all(pixels, (255, 255, 255))
                pixels.fill((255, 0, 0))
                pixels.show()
            ####
            time.sleep(0.5)
        ####
        pixels.fill((0,0,0))
        pixels.show()    
    # needed for persistance before next demo
    time.sleep(2)
    lcd.clear()
    # Start at the second line, fifth column (numbering from zero).
    lcd.set_cursor_pos(0, 4)
    lcd.print("The Forge")
    lcd.set_cursor_pos(1,0)
    lcd.print("Makerspace")
    
def play_UM(filename):
    if filename == None:
        pass
    else:
        decoder.file = open(path + filename, "rb")
        audio.play(decoder)
    ####
    test = True
    while test:
        if (toggle.value == True): #This pauses so long as GP6 is set to HIGH (3.3v); when it goes low, the servo rotates and returns
            angle = 10
            my_servo.angle = angle
            time.sleep(1)
            angle = 85
            my_servo.angle = angle
            test = False
            time.sleep(1)
    ####
    # needed for persistance before next demo
    time.sleep(2)        

def play_hope(filename):
    decoder.file = open(path + filename, "rb")
    audio.play(decoder)
    while audio.playing:
        pass
    ####
    # needed for persistance before next demo
    time.sleep(2)        

def demo_set1():
    while True:
        play_intro("intro_l.mp3")
        play_sounds("sounds.mp3")
        play_lights("lights.mp3", 20)
        play_display("display.mp3", 7)
        play_temp("temp.mp3", 7)
        play_tilt("tap.mp3", 10)
        play_distance("sense_distance.mp3", 30)
        play_UM("UM_respond.mp3")
        play_hope("hope.mp3")
'''
def demo_set2():    
#go into POST-INTRO state: (1) display "Forge" text, (2) blink lights in a pattern, (3) monitor UM switch
    while True:
        play_display(None, 7)
        #play_display("display.mp3", 7)
        play_lights(None, 20)
        #play_lights("lights.mp3", 20)
        play_UM(None)
        #play_UM("UM_respond.mp3")
'''
        
def demo_set2():    
    #go into POST-INTRO state: (1) display "Forge" text, (2) blink lights in a pattern, (3) monitor UM switch
    while True:
        lcd.clear()
        # Start at the second line, fifth column (numbering from zero).
        lcd.set_cursor_pos(0, 4)
        lcd.print("The Forge")
        lcd.set_cursor_pos(1,0)
        lcd.print("Makerspace")
        ORDER = neopixel.GRBW
        count = 1
        with neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER) as pixels:
            for i in range(count):
            # Comment this line out if you have RGBW/GRBW NeoPixels
                pixels.fill((255, 0, 0))
                pixels.show()
                time.sleep(0.5)
            # Comment this line out if you have RGBW/GRBW NeoPixels
                pixels.fill((0, 255, 0))
                pixels.show()
                time.sleep(0.5)
            # Comment this line out if you have RGBW/GRBW NeoPixels
                pixels.fill((0, 0, 255))
                pixels.show()
                time.sleep(0.5)
            #rainbow_cycle(pixels, 0.001)  # rainbow cycle with 1ms delay per step

            pixels.fill((0, 0, 0))
            pixels.show()
    # needed for persistance before next demo
            time.sleep(.5) 
        if (toggle.value == True): #This pauses so long as GP6 is set to HIGH (3.3v); when it goes low, the servo rotates and returns
            angle = 10
            my_servo.angle = angle
            time.sleep(1)
            angle = 85
            my_servo.angle = angle
            time.sleep(1)
    for i in range(duration):
        time.sleep(2)
        if lis3dh.tapped:            
            print("Tapped!")
            decoder.file = open(path + "drum.mp3", "rb")
            audio.play(decoder)
            while audio.playing:
                pass
            time.sleep(.5)
            decoder.file = open(path + "again.mp3", "rb")
            audio.play(decoder)
            time.sleep(.5)            
'''
#Ideally, I would have it such that:
#    (a) it would constantly be sensing whether or not it had been tapped twice
#    (b) it would cycle between (or randomly select) one of six things to say in response to a double-tap
#        (i) ask about whether it has become a drum--drum.mp3
#        (ii) tell the donut kk joke -- dounut.mp3
#        (iii) tell the icecream kk joke -- icecream.mp3
#        (iv) tell the thank you kk joke -- thankyou.mp3
#        (v) tell the vlad kk joke -- vlad.mp3
#        (vi) tell the welcome kk joke --welcome_forge.mp3


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
    import random
    case_value = random.randint(1, 6)
    print ("case value = ", case_value)
    for i in range(duration):
        time.sleep(2)
        if lis3dh.tapped:
            print ("tapped!")
            if case_value == 1:
                decoder.file = open(path + "drum.mp3", "rb")
                audio.play(decoder)
                while audio.playing:
                    pass
            if case_value == 2:
                decoder.file = open(path + "donut.mp3", "rb")
                audio.play(decoder)
                while audio.playing:
                    pass
            if case_value == 3:
                decoder.file = open(path + "icecream.mp3", "rb")
                audio.play(decoder)
                while audio.playing:
                    pass
            if case_value == 4:
                decoder.file = open(path + "thankyou.mp3", "rb")
                audio.play(decoder)
                while audio.playing:
                    pass
            if case_value == 5:
                decoder.file = open(path + "vlad.mp3", "rb")
                audio.play(decoder)
                while audio.playing:
                    pass
            if case_value == 6:
                decoder.file = open(path + "welcome_forge.mp3", "rb")
                audio.play(decoder)
                while audio.playing:
                    pass
'''

