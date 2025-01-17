from board import SCL, SDA, MISO, MOSI
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

i2c = busio.I2C(MISO,MOSI)
display = adafruit_ssd1306.SSD1306_I2C(128,32,i2c)

display.fill(0)

display.show()

image = Image.new("1", (128, 32))
draw = ImageDraw.Draw(image)

# Load a font in 2 different sizes.
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)

# Draw the text
draw.text((0, 0), "bye!", font=font, fill=255)


# display.pagebuffer = image
display.show()
image.show()
display.image(image)
display.show()

# while True:
#     pass