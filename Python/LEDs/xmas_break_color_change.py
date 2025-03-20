import board
import neopixel
import time

PIXEL_NUM = 150

pixels = neopixel.NeoPixel(board.D18, PIXEL_NUM, brightness = 0.2, auto_write = False)

break_length = 15
break_lead = 0
current_strip_color = (255, 0, 0)
changing_strip_color = (0, 255, 0)

pixels.fill((255, 0, 0))
pixels.show()

initial = True

while True:
    if (initial):
        for i in range (0, break_lead, 1):
            pixels[i] = (197, 255, 143)
        
        if (break_lead == break_length - 1):
            initial = False

    else:
        for i in range (break_length):
            pixels[break_lead - i] = (197, 255, 143)

    for i in range (break_lead - break_length):
        pixels[i] = changing_strip_color

    # To change end of strand color from break color to changing color
    if (break_lead < break_length):
        pixels[PIXEL_NUM - break_length + break_lead] = current_strip_color

    break_lead += 1

    if(break_lead >= PIXEL_NUM):
        break_lead = 0
        # Resets pixel color before change of break_lead to 0
        pixels[PIXEL_NUM - break_length -1] = changing_strip_color

        temp = current_strip_color
        current_strip_color = changing_strip_color
        changing_strip_color = temp

    time.sleep(0.05)
    pixels.show()

