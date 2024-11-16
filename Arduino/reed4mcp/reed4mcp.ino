// https://tronixstuff.com/2011/08/26/arduino-mcp23017-tutorial/
// Example 41.3 - Microchip MCP23017 with Arduino


// pins 15~17 to GND, I2C bus address is 0x20
#include "Wire.h"
byte inputs=0;

void setup()
{
  Serial.begin(9600);
  Wire.begin(); // wake up I2C bus
}

void loop()
{
  // read the inputs of bank B
  Wire.beginTransmission(0x20);
  Wire.write(0x13);
  Wire.endTransmission();
  Wire.requestFrom(0x20, 1);
  inputs=Wire.read();

  Serial.println(inputs);

  delay(200); // for debounce
}
