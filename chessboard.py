import board
import adafruit_tca9548a
import time
import board
import busio
from digitalio import Direction, Pull
from adafruit_mcp230xx.mcp23017 import MCP23017
import socket

from board import SCL, SDA, MISO, MOSI
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont




image = Image.new("1", (128, 32))
draw = ImageDraw.Draw(image)

# Load a font in 2 different sizes.
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)

# Draw the text



pola = {
  0:{
        # BEZ 0, 4, 11, 13, 15
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
        #Wszystkie bez 2 i 8
        0:["G5"],
        1:["G6"],
        3:["G8"],
        4:["H5"],
        5:["H6"],
        6:["H7"],
        7:["H8"],
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
        #Bez 1 oraz 12>num>5
        0:["G7"],
        2:["B5"],
        3:["A5"],
        4:["A7"],
        5:["D5"],
        12:["C5"],
        13:["F8"],
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


def setup_led(channel):
    if channel!=5:
        return
    # Initialize the I2C bus:
    i2c = busio.I2C(board.SCL, board.SDA)
    
    display = adafruit_ssd1306.SSD1306_I2C(128,32,i2c)
    return display

def display_text(display,msg):
    # text_displ = clientSocket.recv(1024).decode()
    draw.text((0, 0), msg, font=font, fill=255)
    display.fill(0)
    display.image(image)
    display.show()
    
  
display = None

def read_mcp(channel):
    fields = []
    for pin in pola[channel].keys():
        field, button = pola[channel][pin]
        if button.value:
            fields.append(field)
            #print(channel, "Button #", field, "pressed!", time.time())
            #time.sleep(0.01)
    return fields


host="127.0.0.1"
port = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen(1)

clientSocket, clientAddress = server.accept()

i2c = board.I2C() #uses board.SCL and board.SDA
tca = adafruit_tca9548a.TCA9548A(i2c)
for channel in pola.keys():
    if tca[channel].try_lock():
        for address in tca[channel].scan():
            if address!=0x70:
                setup_mcp(channel)
        tca[channel].unlock()
tca[5].try_lock()
for address in tca[5].scan():
    if address != 0x70:
        display = setup_led(5)
        display_text(display, "msg 123")
    print(address)

_output = "111"
# output = "A2,B2,C2"
# clientSocket.sendall((output).encode("utf-8"))
count = 0
start = time.time()
text_displ = "test"

while True:
    output = []
    for channel in pola.keys():
    #for channel in range(8):
        # if channel ==5:
        #     if tca[channel].try_lock():
        #         text_displ = clientSocket.recv(1024).decode()
        #         draw.text((0, 0), text_displ, font=font, fill=255)
        #         display.fill(0)
        #         display.image(image)
        #         display.show()
        #         tca[channel].unlock()

        if tca[channel].try_lock():
            for address in tca[channel].scan():
                if address!=0x70: #Bylo w tutorialu, nie wiem czy potrzebne, ale dziala
                    for x in read_mcp(channel):
                        output.append(x)
            tca[channel].unlock()
    if len(output)>0:
        print(sorted(output), time.time())
    output = ",".join(output)
    # if time.time() > start + 10:
    #     output = "B2,C2"
    # if time.time() > start + 20:
    #     output = "A4,B2,C2"

    if output != _output:
        if count == 2:
            clientSocket.sendall((output).encode("utf-8"))
            count = 0
            _output = output
        else:
            count += 1
    else:
        count = 0

    clientSocket.settimeout(0.1)  
    try:
        data = clientSocket.recv(1024).decode("utf-8")
        print(data)
    except socket.timeout:
        pass  
    time.sleep(0.1) # Możesz usunąć jak chcesz, bo widzę, że na starej wersji było, a tutaj nie ma
