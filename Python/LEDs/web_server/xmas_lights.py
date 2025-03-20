import board
import neopixel
import time
import random
from light_effects import *
from flask import Flask, render_template, request
import threading
import queue
import os # For CPU temp
import datetime

# TODO: Move all functions to main_functions.py and import them
	# Just for cleanliness' sake
# TODO: Ever since adding timer thread, on page reload it goes to defaults, not current selection
# TODO: Lights won't always go directly off after color fade function was added

app = Flask(__name__, template_folder = '', static_folder = '', static_url_path = '')
is_off_event = threading.Event()

# Workaround for form elements not yet being initialized into form.request
# Won't work with HTML onload because all code files are validated first
# So there was still an error in python refrencing a bad key in form.request
# So default form values are used in a try except block until a form value is changed
# At which point the whole form submits and the elements will be loaded into form.request
default_form_values = {
	"effect": "Color",
	"amount of colors": 1,
	"color0": "#FF4614",
	"color1": "#FF4614",
	"color2": "#FF4614",
	"color3": "#FF4614",
	"color4": "#FF4614",
	"color5": "#FF4614",
	"color6": "#FF4614",
	"color7": "#FF4614",
	"color8": "#FF4614",
	"color9": "#FF4614",
	"mult color style": "alternating",
	"mult block sizes checkbox": False,
	"block size 0": 1,
	"block size 1": 1,
	"block size 2": 1,
	"block size 3": 1,
	"block size 4": 1,
	"block size 5": 1,
	"block size 6": 1,
	"block size 7": 1,
	"block size 8": 1,
	"block size 9": 1,
	"mult brightnesses checkbox": False,
	"brightness0": 50,
	"brightness1": 50,
	"brightness2": 50,
	"brightness3": 50,
	"brightness4": 50,
	"brightness5": 50,
	"brightness6": 50,
	"brightness7": 50,
	"brightness8": 50,
	"brightness9": 50,
	"animated speed slider": 50,
	"on time": 6,
	"off time": 2
	}

# Brightness array used to store potential multiple brightnesses
# So colors can be updated accordingly
brightness_arr = [0.1] * 10
block_size_arr = [1] * 10

def hex_to_grb(hex):
	# Courtesy of: https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
	# Modified to return grb, not rgb
	hex = hex.lstrip('#')	# Removes initial hash
	rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))	# Finds rgb values
	grb = (rgb[1], rgb[0], rgb[2])	# Trades r & g values to create grb tuple
	return grb

color_arr = [hex_to_grb("#FF4614")] * 10

def check_if_off(off, on, x):
    if off <= on:
        return off <= x < on
    else:
        return off < x or x <= on

def time_check(on_time_queue, off_time_queue):
	on_time = get_value("on time")
	off_time = get_value("off time")
	is_off = False
	turning_on = False

	while (True):
		if not on_time_queue.empty():
			on_time = int(on_time_queue.get())
		if not off_time_queue.empty():
			off_time = int(off_time_queue.get())

		current_effect = get_value("effect")
		is_off = check_if_off(off_time, on_time, datetime.datetime.now().hour)

		if is_off:
			is_off_event.set()
			turning_on = False
			if current_effect in looping_effects:
				looping_event.clear()
				static_effect_queue.queue.clear()
				static_effect_queue.put_nowait("bogus") # This is just to pull animated effects out of their inner while loop
			off()
		elif is_off == False and turning_on == False:
			is_off_event.clear()
			turning_on = True

			static_effect_queue.queue.clear()	# Clears bogus call
			if current_effect in looping_effects:
				looping_effect_queue.put_nowait(effect)
				looping_event.set()
			else:
				do_effect()

		time.sleep(600)	# Checks every 10 minutes

		

def looping_effects_analyzer(looping_event, queue_dict, color_arr, brightness_arr):
	# This wait blocks the below code until a selected looping effect triggers it to run
	looping_event.wait()

	# This while loop keeps the thread alive when it is idle
	# Otherwise when the looping event is set to false, it will exit out of its while loop in the effect function
		# Return to this thread function, see there are no more commands
			# And it will die, not to be revived
	# So in other words, don't delete this while loop lol
	while True:
		looping_effect_name = queue_dict["looping effect queue"].get()

		if looping_effect_name == "Random":
			random_colors(brightness_arr, queue_dict)

		if looping_effect_name == "Animated alternating colors":
			animated_alternating_colors(color_arr, block_size_arr, queue_dict)

		if looping_effect_name == "Color fade":
			color_fade(color_arr, queue_dict)

		if looping_effect_name == "Twinkle":
			twinkle(color_arr, block_size_arr, queue_dict)


looping_effects = ["Random", "Animated alternating colors", "Color fade", "Twinkle"]
looping_event = threading.Event()
looping_effect_queue = queue.Queue()
static_effect_queue = queue.Queue()
amount_of_colors_queue = queue.Queue()
animated_effect_speed_queue = queue.Queue()
mult_color_style_queue = queue.Queue()
has_mult_block_sizes_queue = queue.Queue()
# TODO: Do an array dict too
queue_dict = {
	"looping effect queue": looping_effect_queue,
	"static effect queue": static_effect_queue,
	"amount of colors queue": amount_of_colors_queue,
	"animated effect speed queue": animated_effect_speed_queue,
	"mult color style queue": mult_color_style_queue,
	"has mult block sizes queue": has_mult_block_sizes_queue
}
on_time_queue = queue.Queue()
off_time_queue = queue.Queue()
prev_on_time = default_form_values["on time"]
prev_off_time = default_form_values["off time"]
prev_color_amount = default_form_values["amount of colors"]
prev_effect_speed = default_form_values["animated speed slider"]
prev_mult_color_style = default_form_values["mult color style"]
prev_has_mult_block_sizes = default_form_values["mult block sizes checkbox"]
animated_effect_thread = threading.Thread(target = looping_effects_analyzer, name = "looping thread", args = (looping_event, queue_dict, color_arr, brightness_arr,))
time_check_thread = threading.Thread(target = time_check, name = "time check thread", args = (on_time_queue, off_time_queue,), daemon = False)

@app.route("/", methods = ["GET", "POST"])
def action():
	if request.method == 'POST':
		# Copies form values to be used outside this function (in getting values)
			# Form data is local to the app route, so by copying it it can be exported
		global form_data
		form_data = request.form.copy()

		global effect
		effect = get_value("effect")
		
		global has_mult_brightnesses
		global has_mult_block_sizes
		has_mult_brightnesses = get_checkbox_value("mult brightnesses checkbox")
		has_mult_block_sizes = get_checkbox_value("mult block sizes checkbox")

		# This is to debug what keys are actually posted currently to the form
		#print(request.form)

		get_colors()
		get_brightnesses()
		apply_brightnesses()
		get_block_sizes()
		# Prevents effect change causing lights to temporarily be on when they should be off, according to the timer
		if not is_off_event.is_set():
			do_effect()

		if effect in looping_effects:
			static_effect_queue.queue.clear()
			looping_effect_queue.put_nowait(effect)
			# Prevents effect change causing lights to temporarily be on when they should be off, according to the timer
			if not is_off_event.is_set():
				looping_event.set()
		else:
			looping_event.clear()
			static_effect_queue.put(effect)

		# Checking if certain elements have changed to notify the animated effect thread
		current_effect_speed = get_value("animated speed slider")
		global prev_effect_speed
		if not current_effect_speed == prev_effect_speed:
			animated_effect_speed_queue.put_nowait(current_effect_speed)
			prev_effect_speed = current_effect_speed

		current_color_amount = get_value("amount of colors")
		global prev_color_amount
		if not current_color_amount == prev_color_amount:
			amount_of_colors_queue.queue.clear()
			amount_of_colors_queue.put_nowait(current_color_amount)
			prev_color_amount = current_color_amount

		current_mult_color_style = get_value("mult color style")
		# current_block_size = get_value("block size")
		global prev_mult_color_style
		# global prev_block_size
		# If radio buttons have changed
		if not current_mult_color_style == prev_mult_color_style:
			mult_color_style_queue.queue.clear()
			mult_color_style_queue.put_nowait(current_mult_color_style)
			prev_mult_color_style = current_mult_color_style

		global prev_has_mult_block_sizes
		# has_mult_block_sizes defined as global at its declaration
		if not prev_has_mult_block_sizes == has_mult_block_sizes:
			has_mult_block_sizes_queue.queue.clear()
			has_mult_block_sizes_queue.put_nowait(has_mult_block_sizes)
			prev_has_mult_block_sizes = has_mult_block_sizes

		current_on_time = get_value("on time")
		current_off_time = get_value("off time")
		global prev_on_time
		global prev_off_time
		if not current_on_time == prev_on_time:
			on_time_queue.queue.clear()
			on_time_queue.put_nowait(current_on_time)
			prev_on_time = current_on_time
		if not current_off_time == prev_off_time:
			off_time_queue.queue.clear()
			off_time_queue.put_nowait(current_off_time)
			prev_off_time = current_off_time

		pi_temp = get_temp()
		return render_template('index.html', temp = pi_temp)
	
	else:
		pi_temp = get_temp()
		return render_template('index.html', temp = pi_temp)


def get_checkbox_value(checkbox_id):
	# This is a workaround since the checkbox unchecked won't POST data
		# aka wont show up in request dict and will throw an error
	# SO KEEP THIS AS REQUEST.FORM, NOT GET_VALUE
	checkbox_value = False
	try:
		# Converts string "True" to boolean True
		checkbox_value = (form_data[checkbox_id] == "True")
	except:
		checkbox_value = False
	return checkbox_value


# This is a workaround for form elements that haven't yet been initialized by a form submit causing a key error
def get_value(element_name):
	val = 0
	try:
		val = form_data[element_name]
	except Exception as e:
		val = default_form_values[element_name]

	return val

def get_colors():
	for i in range(int(get_value("amount of colors"))):
		col = "color"
		col += str(i)
		color_arr[i] = hex_to_grb(get_value(col))

def get_brightnesses():
	if has_mult_brightnesses:
		for i in range(int(get_value("amount of colors"))):
			b = "brightness"
			b += str(i)
			brightness_arr[i] = float(get_value(b))/100
	else:
		brightness_arr[0] = float(get_value("brightness0"))/100

def apply_brightnesses():
	for i in range(int(get_value("amount of colors"))):

		if has_mult_brightnesses:
			b_index = i
		else:
			b_index = 0

		g = color_arr[i][0] * brightness_arr[b_index]
		r = color_arr[i][1] * brightness_arr[b_index]
		b = color_arr[i][2] * brightness_arr[b_index]
		color_arr[i] = (g, r, b)

def get_block_sizes():
	if has_mult_block_sizes:
		for i in range(int(get_value("amount of colors"))):
			# Keep the space after size!
			bs = "block size "
			bs += str(i)
			block_size_arr[i] = int(get_value(bs))
	else:
		block_size_arr[0] = int(get_value("block size 0"))

def do_effect():
	effect = get_value("effect")

	if effect == "Color":
		color(color_arr, int(get_value("amount of colors")), get_value("mult color style"), has_mult_block_sizes, block_size_arr)

	if effect == "Off":
		off()

def get_temp():
	temp = os.popen('vcgencmd measure_temp').readline()
	return(temp.replace("temp=", "").replace("/n",""))

if __name__ == "__main__":
	if not animated_effect_thread.is_alive():
		animated_effect_thread.start()
	if not time_check_thread.is_alive():
		time_check_thread.start()
	app.run(host='0.0.0.0', port=80, debug = True, threaded = True, use_reloader = False)	# Use reloader set to false to prevent multiple threads being created