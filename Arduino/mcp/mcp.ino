/*
 Example 41.1 - Microchip MCP23017 with Arduino
*/
// pins 15~17 to GND, I2C bus address is 0x20
#include "Wire.h"
void setup()
{
 Wire.begin(); // wake up I2C bus
// set I/O pins to outputs
Wire.beginTransmission(0x20);
 Wire.write(0x01); // IODIRB register
 Wire.write(0x00); // set all of port B to outputs
 Wire.endTransmission();
}
void binaryCount()
{
 for (byte a=0; a<16; a++)
 {
  delay(500);
Wire.beginTransmission(0x20);
 Wire.write(0x13); // GPIOB
 Wire.write(a); // port B
 Wire.endTransmission();
 }
}
void loop()
{
 binaryCount();
 
}
