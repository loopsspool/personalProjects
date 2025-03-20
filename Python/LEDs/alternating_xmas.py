import board
import neopixel
import time

pixels = neopixel.NeoPixel(board.D18, 150, brightness = 0.2, auto_write = False)

while True:
    for i in range(0, 150, 2):
        pixels[i] = (255, 0, 0)

    for i in range(1, 150, 2):
        pixels[i] = (0, 255, 0)

    pixels.show()

    time.sleep(1)

    for i in range(1, 150, 2):
        pixels[i] = (255, 0, 0)

    for i in range(0, 150, 2):
        pixels[i] = (0, 255, 0)

    pixels.show()

    time.sleep(1)
