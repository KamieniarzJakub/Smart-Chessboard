"""
This Raspberry Pi code was developed by newbiely.com
This Raspberry Pi code is made available for public use without any restriction
For comprehensive instructions and wiring diagrams, please visit:
https://newbiely.com/tutorials/raspberry-pi/raspberry-pi-rfid
"""


import RPi.GPIO as GPIO
import mfrc522

# Define the SPI and RST pins for the RC522 module
SPI_PORT = 24
SPI_DEVICE = 24
RST_PIN = 31

# Create an instance of the MFRC522 class
MIFAREReader = mfrc522.MFRC522()

# Function to read the UID from an RFID card and print it in hexadecimal format
def read_uid():
    # Scan for cards
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        # Get the UID of the card
        (status, uid) = MIFAREReader.MFRC522_Anticoll()

        if status == MIFAREReader.MI_OK:
            # Convert the UID bytes to a hexadecimal string
            uid_hex = ''.join(['{:02X}'.format(val) for val in uid])
            print("UID (Hex): " + uid_hex)

# Setup GPIO and initialize the RC522 module
GPIO.setmode(GPIO.BOARD)
GPIO.setup(RST_PIN, GPIO.OUT)
GPIO.output(RST_PIN, GPIO.HIGH)

MIFAREReader.MFRC522_Init()

try:
    print("Press Ctrl+C to exit.")
    while True:
        read_uid()

except KeyboardInterrupt:
    print("\nExiting the program.")
    GPIO.cleanup()
