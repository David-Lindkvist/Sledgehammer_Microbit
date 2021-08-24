# Written by David A. Lindkvist 2021-07-26

# -- Tuneable variables --
delay = 100                 # Millisecond delay for main loop. Signal read frequency = (1000/delay) Hz
input_pin = AnalogPin.P2    # MicroBit pin where sensor is connected
noise_threshold = 4         # Threshold for noise filter. Must be bigger then signal noise.
total_goal = 1000           # Hold the goal for the total. When reached the game starts over.

# -- Other global variables --
signal_base=0               # Hold the signal value from base pressure.
total=0                     # Stores accumulated signal impulses.
last_value=0        	    # Hold the previous signal value. Used to calculate signal change over time.
recording=False             # Used to pause main loop
start_time=0                # Holds the time when last game started
bluetooth_connected=False   # Holds wether a device is connected via bluetooth or not

# Run this on startup
bluetooth.start_uart_service()
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
    elapsed_time = input.running_time()
    recording = True

# Main loop
def on_forever():
    global delay
    if recording:
        basic.pause(delay)
        handle_input()

def handle_input():
    global input_pin
    global noise_threshold
    global signal_base
    global total
    global last_value
    global recording

    signal = pins.analog_read_pin(input_pin)
    

    dT = delay / 1000
    area = dT * ((signal + last_value )/2 - (signal_base + noise_threshold))
    if not area < 0:
        total += area
    display_total()
    message = convert_to_text(signal) + ", "+convert_to_text(Math.round(total))
    write_on_bluetooth(message)

    if total > total_goal:
        recording = False
        time = (input.running_time() - start_time) / 1000
        display_goal_screen(time)
        restart()

def write_on_bluetooth(message):
    if bluetooth_connected:
        bluetooth.uart_write_line(message)

def display_total():
    global total
    global total_goal
    filled_led_rows = Math.round(Math.map(total, 0, total_goal, 0, 5))
    for y in range(5):
        if y < filled_led_rows:
            for x in range(5):
                led.plot(x, y)

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
    

def on_bluetooth_connected():
    global bluetooth_connected
    bluetooth_connected = True
bluetooth.on_bluetooth_connected(on_bluetooth_connected)

def on_bluetooth_disconnected():
    global bluetooth_connected
    bluetooth_connected = False
bluetooth.on_bluetooth_disconnected(on_bluetooth_disconnected)

basic.forever(on_forever)
