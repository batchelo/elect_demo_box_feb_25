import busio
import board
from board import *

i2c = busio.I2C(board.GP11, board.GP10)
i2c.try_lock()
print(i2c.scan())
i2c.unlock()
i2c.deinit()