# Written by David A. Lindkvist 2021-07-26

# -- Tuneable variables --
delay = 10                  
input_pin = AnalogPin.P1
noise_threshold = 2
total_goal = 0
# delay: Millisecond delay for main loop. Signal read frequency = (1000/delay) Hz
# input_pin: MicroBit pin where sensor is connected
# noise_threshold: Threshold for noise filter. Must be bigger then signal noise.

# -- Other global variables (don't change) --
signal_base = pins.analog_read_pin(input_pin)
total = 0
last_value = 0
recording = True
# signal_base: Hold the signal value from base pressure.
# total: Stores accumulated signal impulses.
# last_value: Hold the previous signal value. Used to calculate signal change over time.
# recording: Used to pause main loop

def on_forever():
    global delay
    if recording:
        basic.pause(delay)
        handle_input()
        display_total()

def handle_input():
    global input_pin
    global noise_threshold
    global signal_base
    global total
    global last_value
    signal = pins.analog_read_pin(input_pin)
    dT = delay * 1000
    area = dT * ((signal + last_value )/2 - (signal_base + noise_threshold))
    if not area < 0:
        total += area

def display_total():
    basic.show_string(str(total))

basic.forever(on_forever)