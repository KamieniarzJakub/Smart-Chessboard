import board
import busio
import time
from adafruit_mcp230xx.mcp23017 import MCP23017

i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c)

pin = mcp.get_pin(0)
pin.direction = mcp.DIRECTION_OUTPUT

while True:
    pin.value = True #Turn on
    time.sleep(1)
    pin.value = False #Turn off
    time.sleep(1)