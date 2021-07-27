//  Written by David A. Lindkvist 2021-07-26
//  -- Tuneable variables --
let delay = 10
//  Millisecond delay for main loop. Signal read frequency = (1000/delay) Hz
let input_pin = AnalogPin.P1
//  MicroBit pin where sensor is connected
let noise_threshold = 2
//  Threshold for noise filter. Must be bigger then signal noise.
let total_goal = 1000000
//  Hold the goal for the total. When reached the game starts over.
//  -- Other global variables --
let signal_base = 0
//  Hold the signal value from base pressure.
let total = 0
//  Stores accumulated signal impulses.
let last_value = 0
//  Hold the previous signal value. Used to calculate signal change over time.
let recording = false
//  Used to pause main loop
let start_time = 0
//  Holds the time when last game started
//  Run this on startup
restart()
function restart() {
    
    
    
    
    recording = false
    signal_base = pins.analogReadPin(input_pin)
    total = 0
    last_value = signal_base
    countdown(5)
    let elapsed_time = input.runningTime()
    recording = true
}

function countdown(seconds: number) {
    let i: number;
    for (i = 0; i < seconds; i++) {
        basic.pause(1000)
        basic.showNumber(seconds - i)
    }
    for (i = 0; i < 3; i++) {
        basic.showLeds(`
            # # # # #
            # # # # #
            # # # # #
            # # # # #
            # # # # #
            `)
        basic.clearScreen()
        basic.pause(25)
    }
}

//  Main loop
function handle_input() {
    let recording: boolean;
    let time: number;
    
    
    
    
    
    let signal = pins.analogReadPin(input_pin)
    let dT = delay * 1000
    let area = dT * ((signal + last_value) / 2 - (signal_base + noise_threshold))
    if (!(area < 0)) {
        total += area
    }
    
    if (total > total_goal) {
        recording = false
        time = (input.runningTime() - start_time) / 1000
        display_goal_screen(time)
    }
    
}

function display_total() {
    basic.showString("" + total)
}

function display_goal_screen(time: number) {
    let i: number;
    for (i = 0; i < 6; i++) {
        basic.showLeds(`
            # # # # #
            # # # # #
            # # # # #
            # # # # #
            # # # # #
            `)
        basic.clearScreen()
        basic.pause(25)
    }
    for (i = 0; i < 6; i++) {
        basic.showNumber(time)
        basic.pause(5000)
    }
}

input.onButtonPressed(Button.A, function on_button_pressed_a() {
    restart()
})
basic.forever(function on_forever() {
    
    if (recording) {
        basic.pause(delay)
        handle_input()
        display_total()
    }
    
})
