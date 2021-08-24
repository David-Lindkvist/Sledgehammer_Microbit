# Written by David A. Lindkvist 2021-07-26

# -- Tuneable variables --
delay = 10                  # Millisecond delay for main loop. Signal read frequency = (1000/delay) Hz
input_pin = AnalogPin.P2    # MicroBit pin where sensor is connected
noise_threshold = 2         # Threshold for noise filter. Must be bigger then signal noise.
total_goal = 1000000        # Hold the goal for the total. When reached the game starts over.

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

def handle_input():
    global input_pin
    global noise_threshold
    global signal_base
    global total
    global last_value

    signal = pins.analog_read_pin(input_pin)
    write_on_bluetooth(signal)

    dT = delay * 1000
    area = dT * ((signal + last_value )/2 - (signal_base + noise_threshold))
    if not area < 0:
        total += area
    write_on_bluetooth(total)
    display_total()

    if total > total_goal:
        recording = False
        time = (input.running_time() - start_time) / 1000
        display_goal_screen(time)

def write_on_bluetooth(signal):
    if bluetooth_connected:
        message = convert_to_text(signal)
        bluetooth.uart_write_string(message)

def display_total():
    global total
    filled_led_rows = Math.round(total / 5)
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

LED_row_patterns = ["""
            . . . . .
            . . . . .
            . . . . .
            . . . . .
            . . . . .
            """,
            """
            # # # # #
            . . . . .
            . . . . .
            . . . . .
            . . . . .
            """,
            """
            # # # # #
            . . . . .
            . . . . .
            . . . . .
            # # # # #
            """,
            """
            # # # # #
            # # # # #
            . . . . .
            . . . . .
            # # # # #
            """,
            """
            # # # # #
            # # # # #
            . . . . .
            # # # # #
            # # # # #
            """,
            """
            # # # # #
            # # # # #
            # # # # #
            # # # # #
            # # # # #
            """]