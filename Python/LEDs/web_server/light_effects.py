import board
import neopixel
import time
import random
import math
import colorsys

# TODO: This number is not recognized on startup
num_of_leds = 350
strip = neopixel.NeoPixel(board.D18, num_of_leds, auto_write = False, pixel_order = 'GRB')
amount_of_colors = 1
mult_color_style = "alternating"
has_mult_block_sizes = False
# This controls the time sleep of animated functions
    # Must be a global to accurately store timing data across changes
sleep_amount = 0.5

# NOTE: Functions will get called again every time the form is submitted

############################## STATIC FUNCTIONS ##############################

def off():
    strip.fill((0, 0, 0))
    strip.show()


def color(color_arr, amount_of_colors, mult_color_style, has_mult_block_sizes, block_size_arr):
    color_acc = 0
    i = 0
    # Must be in while loop for dynamic stepping of iterator
    while (i < num_of_leds):
        # Setting block size
        block_size = 1 # For alternating
        if mult_color_style == "block":
            if has_mult_block_sizes:
                block_size = block_size_arr[color_acc]
            else:
                block_size = block_size_arr[0]
        # Putting in each color
        for ii in range(block_size):
            # But only if it's on the strip
            if (i + ii) < num_of_leds:
                strip[i + ii] = color_arr[color_acc]
        # Updating the iterator
        i += block_size
        # Updating the color
        color_acc += 1
        color_acc %= amount_of_colors
        

    strip.show()


############################## ANIMATED FUNCTIONS ##############################

def random_colors(brightness_arr, queue_dict):
    global sleep_amount
    while other_effect_isnt_chosen(queue_dict):
        for i in range (num_of_leds):
            strip[i] = (random.randrange(0, 255) * brightness_arr[0], random.randrange(0, 255) * brightness_arr[0], random.randrange(0, 255) * brightness_arr[0])
        strip.show()

        # Checking if animated speed slider has changed
        if not queue_dict["animated effect speed queue"].empty():
            set_sleep_amount(queue_dict)

        # Prevents stroke-inducing light changes
        if (sleep_amount < 0.07):
            time.sleep(0.07)
        else:
            time.sleep(sleep_amount)


def animated_alternating_colors(color_arr, block_size_arr, queue_dict):
    color_acc = 0 # Color accumulator to animate the effect
    starter_acc = 0
    while other_effect_isnt_chosen(queue_dict):
        check_queues(queue_dict)

        i = 0
        # Must be in while loop for dynamic stepping of iterator
        while (i < num_of_leds):
            # Setting block size
            block_size = 1 # For alternating
            if mult_color_style == "block":
                if has_mult_block_sizes:
                    block_size = block_size_arr[color_acc]
                else:
                    block_size = block_size_arr[0]
            # Putting in each color
            for ii in range(block_size):
                # But only if it's on the strip
                if (i + ii) < num_of_leds:
                    strip[i + ii] = color_arr[color_acc]
            # Updating the iterator
            i += block_size
            # Updating the color
            color_acc += 1
            color_acc %= amount_of_colors

        strip.show()

        # Prevents the change of colors occuring so fast the strip appears one color
        if (sleep_amount < 0.07):
            time.sleep(0.07)
        else:
            time.sleep(sleep_amount)

        # Incrementing the color accumulator to cause the animation effect
        color_acc = 0
        starter_acc += 1
        starter_acc %= amount_of_colors
        color_acc += starter_acc

# TODO: Because of the way this is written (steps dictating "speed")
    # Colors closer together appear to move slower for the same speed as colors spaced farther apart
    # Because they have more distance to cover in the same amount of steps
    # SO ... Make this function work at a consistent speed regardless of the colors present
def color_fade(color_arr, queue_dict):
    color_acc = 0   # Keeps track of current color
    step_acc = 0
    is_adding = False   # Checks whether it should add or subtract accumulator, whichever is closest
    current_color_hsv = grb_to_hsv(color_arr[0])
    next_color_hsv = grb_to_hsv(color_arr[1])
    # Figures out amount of steps based off animated speed change
        # So hue, saturation, and value all get added proportionally
    prev_animated_speed_slider_val = 1 - sleep_amount
    step_min = 40
    step_max = 200
    steps = int(map_range(prev_animated_speed_slider_val, 0, 1, step_max, step_min))

    h_step = (next_color_hsv[0] - current_color_hsv[0])/steps
    s_step = (next_color_hsv[1] - current_color_hsv[1])/steps
    v_step = (next_color_hsv[2] - current_color_hsv[2])/steps

    while other_effect_isnt_chosen(queue_dict):
        check_queues(queue_dict)

        # Resets step range if animated speed slider was moved
        current_animated_speed_slider_val = 1 - sleep_amount
        if not current_animated_speed_slider_val == prev_animated_speed_slider_val:
            steps = int(map_range(1 - sleep_amount, 0, 1, step_max, step_min))
            h_step = (next_color_hsv[0] - current_color_hsv[0])/steps
            s_step = (next_color_hsv[1] - current_color_hsv[1])/steps
            v_step = (next_color_hsv[2] - current_color_hsv[2])/steps
            prev_animated_speed_slider_val = current_animated_speed_slider_val

        if amount_of_colors > 1:
            # TODO: Make it so:
                # If hue is in the high 300s (>340?) and next hue is orange or yellow, add and modulo
                # If hue is in low 0s and next hue is purple, pink, or dark blue (?) subtract it to 360 and the next color

            if not step_acc == steps + 1:
                current_color_hsv = (current_color_hsv[0] + h_step, current_color_hsv[1] + s_step, current_color_hsv[2] + v_step)
                step_acc += 1
                strip.fill(hsv_to_grb(current_color_hsv))
                strip.show()
            else:
                color_acc += 1
                color_acc %= amount_of_colors
                current_color_hsv = grb_to_hsv(color_arr[color_acc])
                next_color_hsv = grb_to_hsv(color_arr[(color_acc + 1) % amount_of_colors])
                h_step = (next_color_hsv[0] - current_color_hsv[0])/steps
                s_step = (next_color_hsv[1] - current_color_hsv[1])/steps
                v_step = (next_color_hsv[2] - current_color_hsv[2])/steps
                step_acc = 0

        
        
# TODO: Causing quick flashing of GREEN (also got a blue once)
    # Isolated to this effect: (ACTUALLY HAPPENS IN COLOR FADE TOO -- but not animated alternating colors)
        # Thread not changing between two different effects
        # And not multiple looping effect threads running
    # Not a color error, color_arr never changes and g/b values never go above 0 on a red
    # color_acc remains correct
    # g, r, b does not go below 0 or above 255
    # Color values are assigned within the amount of leds
    # Doesn't seem to occur in any repeated pattern or at any certain loop count
    # Not related to pi temperature

def twinkle_flashing_diagnostic(pos, col, b, b_d, col_i):
    # Tested with a single color
    if col_i != 0:
        print("color_acc error: ", col_i)

    # This was tested on a dim red to better see flashing, specifically (0, 36, 0) (g, r, b)
    if col[0] > 0 or col[2] > 0:
        print("green and blue values > 0 at position", pos, ": ", col)

    if col[0] < 0 or col[1] < 0 or col[2] < 0:
        print("below 0 color error at position", pos, ": ", col)

    if col[0] > 255 or col[1] > 255 or col[2] > 255:
        print("over 255 color error at position", pos, ": ", col)

    if pos < 0 or pos > 350:
        print("over/under led count error: ", pos)


# TODO: Pixelation still occurs at slow speeds on very dim colors (close to black)
def twinkle(color_arr, block_size_arr, queue_dict):
    brightness = [0] * num_of_leds
    brightness_direction = [0] * num_of_leds
    # Adjusting current slider position to an appropriate range for twinkle
    global sleep_amount
    twinkle_v = (1 - sleep_amount)/15
    prev_sleep_amount = sleep_amount
    max_brightness = 1
    
    # Initializing brightnesses and brightness direction
    for i in range(num_of_leds):
        brightness[i] = random.uniform(.1, max_brightness)
        brightness_direction[i] = random.random() < 0.5

    while other_effect_isnt_chosen(queue_dict):
        check_queues(queue_dict)

        # Checking if animated speed slider has changed
        current_sleep_amount = sleep_amount
        if not current_sleep_amount == prev_sleep_amount:
            twinkle_v = (1 - current_sleep_amount)/15
            prev_sleep_amount = current_sleep_amount

        # So twinkle isn't so incredibly slow and "pixelated"
        if twinkle_v < 0.008:
            twinkle_v = 0.008
        # Or too fast it diminishes the effect
        if twinkle_v > 0.05:
            twinkle_v = 0.05

        color_acc = 0
        i = 0
        while (i < num_of_leds):
            # Setting block size
            block_size = 1 # For alternating
            if mult_color_style == "block":
                if has_mult_block_sizes:
                    block_size = block_size_arr[color_acc]
                else:
                    block_size = block_size_arr[0]
            # Actually doing the colors
            for ii in range(block_size):
                # If the pixel is on the strip
                if (i + ii) < num_of_leds:
                    # Checking bounds
                    if (brightness[i + ii] + twinkle_v) >= max_brightness:
                        brightness_direction[i + ii] = False
                    if (brightness[i + ii] - twinkle_v) <= 0:
                        brightness_direction[i + ii] = True
                    
                    # Incrementing pixel brightness
                    if brightness_direction[i + ii] == True:
                        brightness[i + ii] += twinkle_v
                    else:
                        brightness[i + ii] -= twinkle_v

                    # Applying brightness and color
                    g = math.ceil(color_arr[color_acc][0] * brightness[i + ii])
                    r = math.ceil(color_arr[color_acc][1] * brightness[i + ii])
                    b = math.ceil(color_arr[color_acc][2] * brightness[i + ii])
                    strip[i + ii] = (g, r, b)

                    #twinkle_flashing_diagnostic(i+ii, (g,r,b), brightness[i + ii], brightness_direction[i + ii], color_acc)

            # Updating the accumulator
            i += block_size
            # Updating the color
            color_acc += 1
            color_acc %= amount_of_colors

        strip.show()


def other_effect_isnt_chosen(queue_dict):
    return (queue_dict["looping effect queue"].empty() and queue_dict["static effect queue"].empty())

def check_queues(queue_dict):
    # Checking for colors added/removed
    global amount_of_colors
    if not queue_dict["amount of colors queue"].empty():
        amount_of_colors = int(queue_dict["amount of colors queue"].get())

    # Checking for the style of multiple colors
    global mult_color_style
    if not queue_dict["mult color style queue"].empty():
        mult_color_style = queue_dict["mult color style queue"].get()

    # Checking if it has multiple block sizes
    global has_mult_block_sizes
    if not queue_dict["has mult block sizes queue"].empty():
        has_mult_block_sizes = queue_dict["has mult block sizes queue"].get()

    # Checking if animated speed has changed
    global sleep_amount
    if not queue_dict["animated effect speed queue"].empty():
            set_sleep_amount(queue_dict)

def set_sleep_amount(queue_dict):
    global sleep_amount
    # 1 - to make slider go from slow to fast
    sleep_amount = 1 - float(queue_dict["animated effect speed queue"].get())/100

def grb_to_hsv(grb):
    g = grb[0]/255
    r = grb[1]/255
    b = grb[2]/255
    hsv = colorsys.rgb_to_hsv(r, g, b)
    h = hsv[0] * 360
    s = hsv[1] * 100
    v = hsv[2] * 100
    return (h, s, v)

def hsv_to_grb(hsv):
    h = hsv[0]/360
    s = hsv[1]/100
    v = hsv[2]/100
    rgb = colorsys.hsv_to_rgb(h, s, v)
    r = rgb[0] * 255
    g = rgb[1] * 255
    b = rgb[2] * 255
    return (g, r, b)

# TODO: Make this so ranges can get mapped from say 0-1 to 50-0
# Borrowed from https://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another
# Maps values from one range to another range
def map_range(value, istart, istop, ostart, ostop):
    # Figure out how 'wide' each range is
    ispan = istop - istart
    ospan = ostop - ostart

    # Convert the left range into a 0-1 range (float)
    value_scaled = float(value - istart) / float(ispan)

    # Convert the 0-1 range into a value in the right range.
    return ostart + (value_scaled * ospan)