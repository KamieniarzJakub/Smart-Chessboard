#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""
Scans countinously for cards and prints the UID
"""

__author__ = "Christoph Pranzl"
__version__ = "0.0.5"
__license__ = "GPLv3"

from mfrc522_i2c import MFRC522
import signal

continue_reading = True


# Capture SIGINT for cleanup when script is aborted
def end_read(signal, frame):
    global continue_reading
    print('Ctrl+C captured, ending read')
    continue_reading = False


# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Reader is located at Bus 1, adress 0x28
i2cBus = 13
i2cAddress = 0x50

# Create an object of the class MFRC522
MFRC522Reader = MFRC522(i2cBus, i2cAddress)

version = MFRC522Reader.getReaderVersion()
print(f'MFRC522 Software Version: {version}')

while continue_reading:
    # Scan for cards
    (status, backData, tagType) = MFRC522Reader.scan()
    if status == MFRC522Reader.MIFARE_OK:
        print(f'Card detected, Type: {tagType}')

        # Get UID of the card
        (status, uid, backBits) = MFRC522Reader.identify()
        if status == MFRC522Reader.MIFARE_OK:
            print('Card identified, UID: ', end='')
            for i in range(0, len(uid) - 1):
                print(f'{uid[i]:02x}:', end='')
            print(f'{uid[len(uid) - 1]:02x}')