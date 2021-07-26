//  Written by David A. Lindkvist 2021-07-26
//  -- Tuneable variables --
let delay = 10
let input_pin = AnalogPin.P1
let noise_threshold = 2
let total_goal = 0
//  delay: Millisecond delay for main loop. Signal read frequency = (1000/delay) Hz
//  input_pin: MicroBit pin where sensor is connected
//  noise_threshold: Threshold for noise filter. Must be bigger then signal noise.
//  -- Other global variables (don't change) --
let signal_base = pins.analogReadPin(input_pin)
let total = 0
let last_value = 0
let recording = true
//  signal_base: Hold the signal value from base pressure.
//  total: Stores accumulated signal impulses.
//  last_value: Hold the previous signal value. Used to calculate signal change over time.
//  recording: Used to pause main loop
function handle_input() {
    
    
    
    
    
    let signal = pins.analogReadPin(input_pin)
    let dT = delay * 1000
    let area = dT * ((signal + last_value) / 2 - (signal_base + noise_threshold))
    if (!(area < 0)) {
        total += area
    }
    
}

function display_total() {
    basic.showString("" + total)
}

basic.forever(function on_forever() {
    
    if (recording) {
        basic.pause(delay)
        handle_input()
        display_total()
    }
    
})
