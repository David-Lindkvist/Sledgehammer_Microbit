//  Written by David A. Lindkvist 2021-07-26
//  -- Tuneable variables --
let delay = 10
//  Millisecond delay for main loop. Signal read frequency = (1000/delay) Hz
let input_pin = AnalogPin.P2
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
let bluetooth_connected = false
//  Holds wether a device is connected via bluetooth or not
//  Run this on startup
bluetooth.startUartService()
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
    write_on_bluetooth(signal)
    let dT = delay * 1000
    let area = dT * ((signal + last_value) / 2 - (signal_base + noise_threshold))
    if (!(area < 0)) {
        total += area
    }
    
    write_on_bluetooth(total)
    display_total()
    if (total > total_goal) {
        recording = false
        time = (input.runningTime() - start_time) / 1000
        display_goal_screen(time)
    }
    
}

function write_on_bluetooth(signal: number) {
    let message: string;
    if (bluetooth_connected) {
        message = convertToText(signal)
        bluetooth.uartWriteString(message)
    }
    
}

function display_total() {
    
    let filled_led_rows = Math.round(total / 5)
    for (let y = 0; y < 5; y++) {
        if (y < filled_led_rows) {
            for (let x = 0; x < 5; x++) {
                led.plot(x, y)
            }
        }
        
    }
}

function display_goal_screen(time: number) {
    for (let i = 0; i < 6; i++) {
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

bluetooth.onBluetoothConnected(function on_bluetooth_connected() {
    
    bluetooth_connected = true
})
bluetooth.onBluetoothDisconnected(function on_bluetooth_disconnected() {
    
    bluetooth_connected = false
})
basic.forever(function on_forever() {
    
    if (recording) {
        basic.pause(delay)
        handle_input()
    }
    
})
let LED_row_patterns = [`
            . . . . .
            . . . . .
            . . . . .
            . . . . .
            . . . . .
            `, `
            # # # # #
            . . . . .
            . . . . .
            . . . . .
            . . . . .
            `, `
            # # # # #
            . . . . .
            . . . . .
            . . . . .
            # # # # #
            `, `
            # # # # #
            # # # # #
            . . . . .
            . . . . .
            # # # # #
            `, `
            # # # # #
            # # # # #
            . . . . .
            # # # # #
            # # # # #
            `, `
            # # # # #
            # # # # #
            # # # # #
            # # # # #
            # # # # #
            `]
