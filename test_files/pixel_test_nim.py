import time
import board
import neopixel

pixel_pin = board.GP22

# The number of NeoPixels
num_pixels = 54

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

while True:
    for i in range(num_pixels):
        pixels[i] = pixels.fill(255.0.0)
        pixels.show()
        time.sleep(1)
'''        

    # Increase or decrease to change the speed of the solid color change.
    time.sleep(1)
    pixels.fill(YELLOW)
    pixels.show()
    time.sleep(1)
    pixels.fill(GREEN)
    pixels.show()
    time.sleep(1)
    pixels.fill(CYAN)
    pixels.show()
    time.sleep(1)
    pixels.fill(BLUE)
    pixels.show()
    time.sleep(1)
    pixels.fill(PURPLE)
    pixels.show()
    time.sleep(1)

    
    
    # Comment this line out if you have RGBW/GRBW NeoPixels
    for i in range (54):
    pixels[i] = pixels.fill((255,0,0))
    pixels.show()
    time.sleep(1)

    pixels[i] = pixels.fill((255,0,0,))
    pixels.show()
    i= i + 1
    time.sleep(1)

54:
    pixels[i] = pixels.fill((255, 0, 0))
    pixels.show()
    i = i+1
    time.sleep(1)
    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(2)
    # Comment this line out if you have RGBW/GRBW NeoPixels
    pixels.fill((0, 0, 255))
    pixels.show()
    time.sleep(2)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
    
'''
    
