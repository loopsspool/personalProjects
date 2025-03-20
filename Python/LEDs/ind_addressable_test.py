import board
import neopixel
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(board.D18, 150, brightness = 0.2)

for i in range(0, 150, 2):
    pixels[i] = (255, 0, 0)

for i in range(1, 150, 2):
    pixels[i] = (0, 255, 0)