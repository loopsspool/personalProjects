import board
import neopixel
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(board.D18, 150, brightness = 0.2)

pixels.fill((255, 255, 255))