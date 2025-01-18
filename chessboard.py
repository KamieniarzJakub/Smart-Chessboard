#Część 1 - odczyt oraz wyświetlanie informacji o zalecanym ruchu

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

# Załadowanie czcionki
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)

display_pins = [4, 5]  # Definicja pinów dla wyświetlaczy LED

# Słownik przechowujący konfigurację kanałów i odpowiadających im pinów
pola = {
  0: {
        # Wykluczone: 0, 4, 11, 13, 15
        1: ["C6"],
        2: ["C7"],
        3: ["C8"],
        5: ["D6"],
        6: ["D7"],
        7: ["D8"],
        8: ["B8"],
        9: ["B7"],
        10: ["B6"],
        12: ["A8"],
        14: ["A6"]
        },
    1: {
        # Wykluczone: 2, 8
        0: ["G5"],
        1: ["G6"],
        3: ["G8"],
        4: ["H5"],
        5: ["H6"],
        6: ["H7"],
        7: ["H8"],
        9: ["F7"],
        10: ["F6"],
        11: ["F5"],
        12: ["E8"],
        13: ["E7"],
        14: ["E6"],
        15: ["E5"]
    },
    2: {
        # Wszystkie piny
        0: ["G4"],
        1: ["G3"],
        2: ["G2"],
        3: ["G1"],
        4: ["H4"],
        5: ["H3"],
        6: ["H2"],
        7: ["H1"],
        8: ["F1"],
        9: ["F2"],
        10: ["F3"],
        11: ["F4"],
        12: ["E1"],
        13: ["E2"],
        14: ["E3"],
        15: ["E4"]
    },
    6: {
        # Wykluczone: 3, 4
        0: ["C4"],
        1: ["C3"],
        2: ["C2"],
        5: ["D3"],
        6: ["D2"],
        7: ["D1"],
        8: ["B1"],
        9: ["B2"],
        10: ["B3"],
        11: ["B4"],
        12: ["A4"],
        13: ["A3"],
        14: ["A2"],
        15: ["A1"]
        },
    7: {
        # Wykluczone: 1 oraz 6-11
        0: ["G7"],
        2: ["B5"],
        3: ["A5"],
        4: ["A7"],
        5: ["D5"],
        12: ["C5"],
        13: ["F8"],
        14: ["C1"],
        15: ["D4"]
        }
}

# Funkcja inicjalizująca układ MCP23017 dla danego kanału
def setup_mcp(channel):
    # Inicjalizacja magistrali I2C
    i2c = busio.I2C(board.SCL, board.SDA)
    # Inicjalizacja układu MCP23017
    mcp = MCP23017(i2c)

    # Konfiguracja pinów jako wejścia z podciągnięciem do VCC
    for pin in pola[channel].keys():
        pola[channel][pin].append(mcp.get_pin(pin))
        pola[channel][pin][-1].direction = Direction.INPUT
        pola[channel][pin][-1].pull = Pull.UP

# Funkcja konfigurująca wyświetlacz OLED
def setup_led():
    i2c = busio.I2C(board.SCL, board.SDA)
    display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
    return display

# Funkcja do wyświetlania tekstu na wyświetlaczu OLED
def display_text(display, msg):
    image = Image.new("1", (128, 32))  # Utworzenie czarno-białego obrazu
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), msg, font=font, fill=255)  # Rysowanie tekstu
    display.fill(0)  # Czyszczenie wyświetlacza
    display.image(image)  # Przesłanie obrazu na wyświetlacz
    display.show()

# Tablica przechowująca wyświetlacze LED
led_displays = [None, None]

# Funkcja odczytująca stany przycisków dla danego kanału
def read_mcp(channel):
    fields = []
    for pin in pola[channel].keys():
        field, button = pola[channel][pin]
        if button.value:  # Sprawdzenie, czy przycisk jest wciśnięty
            fields.append(field)
    return fields

# Konfiguracja serwera sieciowego
host = "127.0.0.1"
port = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen(1)

clientSocket, clientAddress = server.accept()  # Oczekiwanie na połączenie klienta

i2c = board.I2C()  # Inicjalizacja magistrali I2C
tca = adafruit_tca9548a.TCA9548A(i2c)  # Multiplexer TCA9548A

# Inicjalizacja kanałów MCP23017
for channel in pola.keys():
    if tca[channel].try_lock():
        for address in tca[channel].scan():
            if address != 0x70:
                setup_mcp(channel)
        tca[channel].unlock()

# Inicjalizacja wyświetlaczy LED
for i in display_pins:
    while not tca[i].try_lock():
        pass
    for address in tca[i].scan():
        if address != 0x70:
            led_displays[i % 2] = setup_led()
            display_text(led_displays[i % 2], "Loading...")
    tca[i].unlock()

# Wstępna ustalenie wartości początkowych
_output = "111" 
count = 0
start = time.time()

while True:
    output = []
    for channel in pola.keys():
        if tca[channel].try_lock():
            for address in tca[channel].scan():
                if address != 0x70:  # Filtracja adresów
                    for x in read_mcp(channel):
                        output.append(x)
            tca[channel].unlock()
    if len(output) > 0:
        print(sorted(output), time.time())
    output = ",".join(output)

    if output != _output:
        if count == 1:
            clientSocket.sendall((output).encode("utf-8"))  # Wysyłanie danych do klienta
            count = 0
            _output = output
        else:
            count += 1
    else:
        count = 0

    clientSocket.settimeout(0.1)  # Ustawienie timeoutu dla socketu
    try:
        data = clientSocket.recv(1024).decode("utf-8")
        print(data)
        for i in display_pins:
            if tca[i].try_lock():
                for address in tca[i].scan():
                    if address != 0x70:
                        display_text(led_displays[i % 2], data)  # Wyświetlanie danych
                tca[i].unlock()
    except socket.timeout:
        pass

    time.sleep(0.1)
