import time
import board
import busio
import digitalio
from digitalio import DigitalInOut, Direction
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface

toggle = digitalio.DigitalInOut(board.GP2)
toggle.direction = digitalio.Direction.INPUT

i2c_d = busio.I2C(scl=board.GP11, sda=board.GP10)
lcd = LCD(I2CPCF8574Interface(i2c_d, 0x23), num_rows=2, num_cols=16)
lcd.clear()

if toggle.value == True:
    lcd.set_cursor_pos(0, 0)
    lcd.print("audio sig")
    lcd.set_cursor_pos(1, 0)
    lcd.print("HIGH")
    time.sleep(5)
elif toggle.value == False:
    lcd.set_cursor_pos(0, 0)
    lcd.print("audio sig")
    lcd.set_cursor_pos(1, 0)
    lcd.print("LOW")
    time.sleep(5)
else:
    lcd.set_cursor_pos(0, 0)
    lcd.print("audio sig")
    lcd.set_cursor_pos(1, 0)
    lcd.print("not detected")
    time.sleep(5)