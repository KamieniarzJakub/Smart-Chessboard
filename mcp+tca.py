import board
import adafruit_tca9548a
import time
import board
import busio
from digitalio import Direction, Pull
from adafruit_mcp230xx.mcp23017 import MCP23017

pola = [["G4", "G3", "G2", "G1", "H4", "H3", "H2", "H1", "F1", "F2", "F3", "F4", "E1", "E2", "E3", "E4"],
        ["D4", "D3", "D2", "D1", "C4", "C3", "C2", "C1", "B1", "B2", "B3", "B4", "A1", "A2", "A3", "A4"]]

def read_mcp(channel):
    # Initialize the I2C bus:
    i2c = busio.I2C(board.SCL, board.SDA)
    # Initialize the MCP23017 chip on the bonnet
    mcp = MCP23017(i2c)

    pins = []
    for pin in range(0, 16):
        pins.append(mcp.get_pin(pin))
    
    # Set all the port pins to input, with pullups!
    for pin in pins:
        pin.direction = Direction.INPUT
        pin.pull = Pull.UP

    for num, button in enumerate(pins):
        if button.value and not((channel==3 and (num==13 or num==15 or num==4))):
            print(channel,"Button #", num, "pressed!", time.time())
            time.sleep(0.1)



i2c = board.I2C() #uses board.SCL and board.SDA
tca = adafruit_tca9548a.TCA9548A(i2c)
while True:
    for channel in range(8):
        if tca[channel].try_lock():
            for address in tca[channel].scan():
                if address!=0x70: #Bylo w tutorialu, nie wiem czy potrzebne, ale dziala
                    read_mcp(channel)
            tca[channel].unlock()


