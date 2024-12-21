import board
import adafruit_tca9548a
import time
import board
import busio
from digitalio import Direction, Pull
from adafruit_mcp230xx.mcp23017 import MCP23017

pola = {
  0:{
        # BEZ 4, 11, 13, 15
        0:["C5"],
        1:["C6"],
        2:["C7"],
        3:["C8"],
        5:["D6"],
        6:["D7"],
        7:["D8"],
        8:["B8"],
        9:["B7"],
        10:["B6"],
        12:["A8"],
        14:["A6"]
        },
    1:{
        #Wszystkie bez 2
        0:["G5"],
        1:["G6"],
        3:["G8"],
        4:["H5"],
        5:["H6"],
        6:["H7"],
        7:["H8"],
        8:["F8"],
        9:["F7"],
        10:["F6"],
        11:["F5"],
        12:["E8"],
        13:["E7"],
        14:["E6"],
        15:["E5"]
    },
    2:{
        #Wszystkie
        0:["G4"],
        1:["G3"],
        2:["G2"],
        3:["G1"],
        4:["H4"],
        5:["H3"],
        6:["H2"],
        7:["H1"],
        8:["F1"],
        9:["F2"],
        10:["F3"],
        11:["F4"],
        12:["E1"],
        13:["E2"],
        14:["E3"],
        15:["E4"]
    },
    6:{
        #Wszystkie bez 3 i 4
        0:["C4"],
        1:["C3"],
        2:["C2"],
        5:["D3"],
        6:["D2"],
        7:["D1"],
        8:["B1"],
        9:["B2"],
        10:["B3"],
        11:["B4"],
        12:["A4"],
        13:["A3"],
        14:["A2"],
        15:["A1"]
        },
    7:{
        #Bez 1 oraz 14>num>5
        0:["G7"],
        2:["B5"],
        3:["A5"],
        4:["A7"],
        5:["D5"],
        14:["C1"],
        15:["D4"]
        }
}

def setup_mcp(channel):
    # Initialize the I2C bus:
    i2c = busio.I2C(board.SCL, board.SDA)
    # Initialize the MCP23017 chip on the bonnet
    mcp = MCP23017(i2c)

    for pin in pola[channel].keys():
        pola[channel][pin].append(mcp.get_pin(pin))
        pola[channel][pin][-1].direction = Direction.INPUT
        pola[channel][pin][-1].pull = Pull.UP



def read_mcp(channel):
    fields = []
    for pin in pola[channel].keys():
        field, button = pola[channel][pin]
        if button.value:
            fields.append(field)
            #print(channel, "Button #", field, "pressed!", time.time())
            time.sleep(0.1)
    return fields



i2c = board.I2C() #uses board.SCL and board.SDA
tca = adafruit_tca9548a.TCA9548A(i2c)
for channel in pola.keys():
    if tca[channel].try_lock():
        for address in tca[channel].scan():
            if address!=0x70:
                setup_mcp(channel)
        tca[channel].unlock()

while True:
    output = []
    for channel in pola.keys():
    #for channel in range(8):
        if tca[channel].try_lock():
            for address in tca[channel].scan():
                if address!=0x70: #Bylo w tutorialu, nie wiem czy potrzebne, ale dziala
                    for x in read_mcp(channel):
                        output.append(x)
            tca[channel].unlock()
    if len(output)>0:
        print(sorted(output), time.time())
    print(",".join(output))
    with open("move.txt", "w+") as file:
        file.write(",".join(output))

