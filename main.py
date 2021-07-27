# Written by David A. Lindkvist 2021-07-26

# -- Tuneable variables --
delay = 10                  # Millisecond delay for main loop. Signal read frequency = (1000/delay) Hz
input_pin = AnalogPin.P1    # MicroBit pin where sensor is connected
noise_threshold = 2         # Threshold for noise filter. Must be bigger then signal noise.
total_goal = 1000000        # Hold the goal for the total. When reached the game starts over.

# -- Other global variables --
signal_base=0               # Hold the signal value from base pressure.
total=0                     # Stores accumulated signal impulses.
last_value=0        	    # Hold the previous signal value. Used to calculate signal change over time.
recording=False             # Used to pause main loop
start_time=0                # Holds the time when last game started

# Run this on startup
restart()
def restart():
    global signal_base
    global total
    global last_value
    global recording
    
    recording = False
    signal_base = pins.analog_read_pin(input_pin)
    total = 0
    last_value = signal_base
    countdown(5)
    elapsed_time = input.running_time()
    recording = True

def countdown(seconds):
    for i in range(seconds):
        basic.pause(1000)
        basic.show_number(seconds - i)
    for i in range(3):
        basic.show_leds("""
            # # # # #
            # # # # #
            # # # # #
            # # # # #
            # # # # #
            """)
        basic.clear_screen()
        basic.pause(25)

# Main loop
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

    if total > total_goal:
        recording = False
        time = (input.running_time() - start_time) / 1000
        display_goal_screen(time)

def display_total():
    basic.show_string(str(total))

def display_goal_screen(time):
    for i in range(6):
        basic.show_leds("""
            # # # # #
            # # # # #
            # # # # #
            # # # # #
            # # # # #
            """)
        basic.clear_screen()
        basic.pause(25)
    
    for i in range(6):
        basic.show_number(time)
        basic.pause(5000)

def on_button_pressed_a():
    restart()
    
input.on_button_pressed(Button.A, on_button_pressed_a)
basic.forever(on_forever)