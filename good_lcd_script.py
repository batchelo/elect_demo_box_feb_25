import board
import busio

from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface

from lcd.lcd import CursorMode

i2c_d = busio.I2C(scl=board.GP11, sda=board.GP10)
lcd = LCD(I2CPCF8574Interface(i2c_d, 0x23), num_rows=2, num_cols=16)
#lcd.backlight(0x08)

lcd.clear()

# Start at the second line, fifth column (numbering from zero).
lcd.set_cursor_pos(0, 3)
lcd.print("The Forge")
lcd.set_cursor_pos(1, 2)
lcd.print("Makerspace")

# Make the cursor visible as a line.
#lcd.set_cursor_mode(CursorMode.LINE)