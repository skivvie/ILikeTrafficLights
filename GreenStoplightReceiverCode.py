"""
LOST HWY Stop Light Receiver Code v1
Waits for R, Y, G, B, or O (off) packets from the Transmitter and turns on the corresponding lights
"""

import board
import digitalio
import neopixel
import adafruit_rfm9x

# Setup up output relay pins
red_relay = digitalio.DigitalInOut(board.D5)
red_relay.direction = digitalio.Direction.OUTPUT
yellow_relay = digitalio.DigitalInOut(board.D6)
yellow_relay.direction = digitalio.Direction.OUTPUT
green_relay = digitalio.DigitalInOut(board.D9)
green_relay.direction = digitalio.Direction.OUTPUT

# Set up NeoPixel.
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixel.brightness = 0.5

# Define radio frequency in MHz. Must match your
# module. Can be a value like 915.0, 433.0, etc.
RADIO_FREQ_MHZ = 915.0

# Define Chip Select and Reset pins for the radio module.
CS = digitalio.DigitalInOut(board.RFM_CS)
RESET = digitalio.DigitalInOut(board.RFM_RST)

# Initialise RFM95 radio
rfm95 = adafruit_rfm9x.RFM9x(board.SPI(), CS, RESET, RADIO_FREQ_MHZ)

# Wait to receive packets.
print("Waiting for packets...")
while True:
    # Look for a new packet - wait up to 5 seconds:
    packet = rfm95.receive(timeout=5.0)
    # If no packet was received during the timeout then None is returned.
    if packet is not None:
        print("Received a packet! Changing color!")
        # If the received packet is b'red'...
        if packet == b'R':
            # set NeoPixel LED color to red.
            pixel.fill((255, 0, 0))
            # turn on the RED Relay and the others off
            yellow_relay.value = False
            green_relay.value = False
            red_relay.value = True
            print("RED!")
        elif packet == b'Y':
            pixel.fill((255, 255, 0))
            red_relay.value = False
            green_relay.value = False
            yellow_relay.value = True
            print("YELLOW!")
        elif packet == b'G':
            pixel.fill((0, 255, 0))
            red_relay.value = False
            yellow_relay.value = False
            green_relay.value = True
            print("GREEN!")
        elif packet == b'B':
            pixel.fill((0, 0, 255))
            red_relay.value = True
            yellow_relay.value = True
            green_relay.value = True
            print("BLUE!")
         elif packet == b'O':
            pixel.fill((0, 0, 255))
            red_relay.value = False
            yellow_relay.value = False
            green_relay.value = False
            print("BLUE!")           
        else:
            print("No packets")
