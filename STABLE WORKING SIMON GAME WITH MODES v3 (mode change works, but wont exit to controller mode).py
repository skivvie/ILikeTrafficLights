"""
First attempt at simon game
"""

import random
import board
import digitalio
import neopixel
import adafruit_rfm9x
import time
import audiocore
import audiopwmio

# Set up SIMON input buttons
RedButton = digitalio.DigitalInOut(board.TX)
RedButton.direction = digitalio.Direction.INPUT
RedButton.pull = digitalio.Pull.UP
YellowButton = digitalio.DigitalInOut(board.RX)
YellowButton.direction = digitalio.Direction.INPUT
YellowButton.pull = digitalio.Pull.UP
GreenButton = digitalio.DigitalInOut(board.D25)
GreenButton.direction = digitalio.Direction.INPUT
GreenButton.pull = digitalio.Pull.UP
BlueButton = digitalio.DigitalInOut(board.D24)
BlueButton.direction = digitalio.Direction.INPUT
BlueButton.pull = digitalio.Pull.UP

# Setup up LED output pins
RedLED = digitalio.DigitalInOut(board.D5)
RedLED.direction = digitalio.Direction.OUTPUT
YellowLED = digitalio.DigitalInOut(board.D6)
YellowLED.direction = digitalio.Direction.OUTPUT
GreenLED = digitalio.DigitalInOut(board.D9)
GreenLED.direction = digitalio.Direction.OUTPUT
BlueLED = digitalio.DigitalInOut(board.D10)
BlueLED.direction = digitalio.Direction.OUTPUT

# Initialize the mode button
mode_button = digitalio.DigitalInOut(board.D13)
mode_button.direction = digitalio.Direction.INPUT
mode_button.pull = digitalio.Pull.UP

# Initialize the modes
modes = ['controller_mode', 'simon_mode', 'silent_simon_mode']
mode = modes.index('controller_mode')  # Start in Controller Mode

# Setup Sounds
meow = open("meow1.wav", "rb")
bark = open("bark1.wav", "rb")
fart = open("fart1.wav", "rb")
blip = open("blip.wav", "rb")
meowWav = audiocore.WaveFile(meow)
barkWav = audiocore.WaveFile(bark)
fartWav = audiocore.WaveFile(fart)
blipWav = audiocore.WaveFile(blip)
audio = audiopwmio.PWMAudioOut(board.A0)

# Define the buttons and LEDs in a list for easy access
buttons = [RedButton, YellowButton, GreenButton, BlueButton]
leds = [RedLED, YellowLED, GreenLED, BlueLED]
sounds = [meowWav, barkWav, fartWav, blipWav]

# Initialize the delay time and round counter
delay_time = 0.5
round_counter = 0

while True:  # Outer loop to restart the game
    # Check if the mode button is pressed
    if not mode_button.value:
        mode = (mode + 1) % len(modes)  # Go to the next mode, wrap back to 0 if it's the last mode
        time.sleep(0.5)  # Debounce the button press
        continue  # Skip the rest of the loop and start over with the new mode

    if modes[mode] == 'controller_mode':
        # First mode: light up the LED and play the sound when the button is pressed
        for i, button in enumerate(buttons):
            if not button.value:  # Button is pressed (value is False when pressed because of pull-up resistor)
                leds[i].value = True  # Light up the LED when the button is pressed
                audio.play(sounds[i])  # Play the sound when the button is pressed
                while not button.value:  # Keep the LED lit as long as the button is pressed
                    pass
                leds[i].value = False  # Turn off the LED when the button is released
    
    elif modes[mode] == 'simon_mode' or modes[mode] == 'silent_simon_mode':
        # Game sequence
        game_sequence = []

        # Game state
        game_over = False

        while not game_over:
            # Add a new color to the sequence at the start of each round
            new_color = random.choice(range(4))
            game_sequence.append(new_color)

            # Play the sequence to the player
            for color in game_sequence:
                leds[color].value = True
                if modes[mode] == 'simon_mode':
                    audio.play(sounds[color])
                time.sleep(delay_time)
                leds[color].value = False
                time.sleep(delay_time)

            # Get the player's response
            for color in game_sequence:
                button_pressed = False
                while not button_pressed:
                    for i, button in enumerate(buttons):
                        if not button.value:  # Button is pressed
                            button_pressed = True
                            if i != color:  # Player pressed the wrong button
                                game_over = True
                            else:
                                leds[i].value = True  # Light up the LED when the button is pressed
                                if modes[mode] == 'simon_mode':
                                    audio.play(sounds[i])  # Play the sound when the button is pressed
                                while not button.value:  # Keep the LED lit as long as the button is pressed
                                    pass
                                leds[i].value = False  # Turn off the LED when the button is released
                            break
                    if not mode_button.value:  # Mode button is pressed
                        mode = (mode + 1) % len(modes)  # Change the mode
                        if modes[mode] == 'silent_simon_mode':  # If the new mode is 'silent_simon_mode'
                            game_sequence = []  # Reset the game sequence
                            game_over = False  # Reset the game state
                            delay_time = 0.5  # Reset the delay time
                            round_counter = 0  # Reset the round counter
                        break  # Exit the inner loop
                if not mode_button.value or game_over:
                    break  # Exit the outer loop

            # Add a delay after the user inputs the correct sequence
            if not game_over:
                time.sleep(1)
                round_counter += 1
                if round_counter % 2 == 0:  # After every 2 rounds
                    delay_time *= 0.8  # Decrease the delay time by 20%

        # Game over, flash all LEDs and play the fart sound
        if game_over:
            for _ in range(6):
                for led in leds:
                    led.value = True
                time.sleep(0.1)
                for led in leds:
                    led.value = False
                time.sleep(0.1)
            audio.play(sounds[2])  # Play the fart sound

        # Reset the delay time and round counter for the next game
        delay_time = 0.5
        round_counter = 0

        # Delay before restarting the game
        time.sleep(5)