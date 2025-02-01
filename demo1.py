################################################################################
# DEMO1.PY
################################################################################
import time
import board
import neopixel


import asyncio

import digitalio
from audiomp3 import MP3Decoder
from audiopwmio import PWMAudioOut as AudioOut




#for the liquid crystal display
import busio
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface
from lcd.lcd import CursorMode



#regarding the LCD display
i2c_d = busio.I2C(scl=board.GP11, sda=board.GP10)
lcd = LCD(I2CPCF8574Interface(i2c_d, 0x27), num_rows=2, num_cols=16)



#for the temp/humidity sensor
import adafruit_dht
#regarding the temp_humidity module
dhtDevice = adafruit_dht.DHT11(board.GP4) # specs for the temp/hum module


#



#
#play_distance("sense_distance.mp3")
#play_UM("UM_respond.mp3")
#play_hope("hope.mp3")


audio = AudioOut(board.GP17)
path = "sounds/"

# initialization
decoder = MP3Decoder("sounds/intro_l.mp3")


################################################################################
def play_intro(filename, decoder):
    mp3_file = open(path + filename, "rb")
    
    decoder.file = open(path + filename, "rb")

    audio.play(decoder)
    while audio.playing:
        pass
    
################################################################################
def play_sounds(filename, decoder):
    decoder.file = open(path + filename, "rb")
    audio.play(decoder)
    while audio.playing:
        pass
################################################################################
# ORDER = neopixel.GRBW
def wheel_lights(pos):
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
            return (r, g, b) if neopixel.GRBW in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

pixels = neopixel.NeoPixel(board.GP22, 54, brightness=0.2, auto_write=False, pixel_order=neopixel.GRBW)        
def rainbow_cycle(num_pixels, wait):
    global pixels
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel_lights(pixel_index & 255)
    pixels.show()
    time.sleep(wait)

lights_count = 0
async def lights_demo(interval, count):
    global lights_count
    global pixels
    for i in range(count):
        # Comment this line out if you have RGBW/GRBW NeoPixels
        pixels.fill((255, 0, 0))
        pixels.show()
        await asyncio.sleep(interval)  # Don't forget the "await"!
        #await asyncio.sleep(interval)  # Don't forget the "await"!
        # Comment this line out if you have RGBW/GRBW NeoPixels
        pixels.fill((0, 255, 0))
        pixels.show()
        await asyncio.sleep(interval)  # Don't forget the "await"!
        #await asyncio.sleep(interval)  # Don't forget the "await"!
        # Comment this line out if you have RGBW/GRBW NeoPixels
        pixels.fill((0, 0, 255))
        pixels.show()
        await asyncio.sleep(interval)  # Don't forget the "await"!
        #rainbow_cycle(54, 0.001)  # rainbow cycle with 1ms delay per step
        # blinky effect here
        # fix this later
        '''
        for j in range(255):
            for i in range(54):
                pixel_index = (i * 256 // 54) + j
                pixels[i] = wheel_lights(pixel_index & 255)
                pixels.show()
        await asyncio.sleep(interval)  # Don't forget the "await"!
        '''
        print('count', i)
        
    pixels.fill((0, 0, 0))
    pixels.show()

async def play_lights_demo(filename):
    # light and mp3 together
    decoder.file = open(path + filename, "rb")
    audio.play(decoder)
    lights_demo_task = asyncio.create_task(lights_demo(0.1, 20))
    await asyncio.gather(lights_demo_task)  # Don't forget "await"!
    ####

################################################################################
def play_display(filename):
    decoder.file = open(path + filename, "rb")
    audio.play(decoder)
    while audio.playing:
        lcd.clear()
    # Start at the second line, fifth column (numbering from zero).
        lcd.set_cursor_pos(0, 4)
        lcd.print("The Forge")
        lcd.set_cursor_pos(1,3)
        lcd.print("Makerspace")
    
################################################################################
def play_temp(filename):
  try:
      # Print the values to the display
      temperature_c = dhtDevice.temperature
      temperature_f = temperature_c * (9 / 5) + 32
      humidity = dhtDevice.humidity
      lcd.clear()
      # Start at the second line, fifth column (numbering from zero).
      lcd.set_cursor_pos(0, 0)
      lcd.print("Temp is:  "+str(temperature_f))
      lcd.set_cursor_pos(1,0)
      lcd.print("Humidity is: "+str(humidity))
            
  except RuntimeError as error:
      # Errors happen fairly often, DHT's are hard to read, just keep going
      print(error.args[0])
      time.sleep(2.0)
        
  except Exception as error:
      #print(" hi NIM")
      dhtDevice.exit()
      
  # play audio    
  decoder.file = open(path + filename, "rb")
  audio.play(decoder)
  
      
            

################################################################################

        
def demo1_main():
    #play_intro("intro_l.mp3", decoder)
    #play_sounds("sounds.mp3", decoder)
    #asyncio.run(play_lights_demo("lights.mp3"))
    play_display("display.mp3")
    time.sleep(3)
    play_temp("temp.mp3")
    time.sleep(3)
    play_tilt("tilt.mp3")
    #asyncio.run(play_lights_demo("lights.mp3"))

    
    print("done")

#asyncio.run(play_lights_demo("lights.mp3"))
demo1_main() 
#asyncio.run(demo1_main())
