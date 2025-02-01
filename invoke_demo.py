"""Tests whether GP2 is pulled high.  This only happens when the audio switch is turned on.  Thus, I can use this input
to decide whether to enter the demo mode or go into the standby loop mode.  This should be tested at the start of the program.
if it is high, then the audio has been turned on, thus the user wants the demo mode.  If the audio switch is off, then the
user is signaling that they want the box to directly enter into the standby mode."""
import time
import board
import busio
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface
from lcd.lcd import CursorMode
import digitalio
from digitalio import DigitalInOut, Direction, Pull

# create an input signal on Pin GP2.

is_demo = digitalio.DigitalInOut(board.GP2)
is_demo.switch_to_input(pull=digitalio.Pull.DOWN)
#is_demo.pull = digitalio.Pull.DOWN

# the digitalio documentation says that the pulldown resistor is weak and useless
# therefore, I need to insert a "strong" external pull-down resistor.  They suggest 8.2 k oms or less.  Let's see
# if the internal pulldown is sufficient for this signal purpose.

#instantiate a lcd object

i2c_d = busio.I2C(scl=board.GP11, sda=board.GP10)
lcd = LCD(I2CPCF8574Interface(i2c_d, 0x23), num_rows=2, num_cols=16)

if board.GP2 == True:
    #run demo program
    lcd.clear()
    lcd.set_cursor_pos(0, 0)
    lcd.print("switch high")
    lcd.set_cursor_pos(1, 0)
    lcd.print("run demo")
    time.sleep(5)
    
else:
    #run standby loop
    lcd.clear()
    lcd.set_cursor_pos(0, 0)
    lcd.print("switch low")
    lcd.set_cursor_pos(1, 0)
    lcd.print("run standby")
    time.sleep(5)
    
