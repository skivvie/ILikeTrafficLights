This is an Adafruit Feather RP2040 with RFM95 LoRa Radio (https://learn.adafruit.com/feather-rp2040-rfm95) that is inside of a hacked Simon controller. It talks to another of the same that is inside a traffic light. 

The current code is there for these things which work: 
1. Control the light directly. Press Red button, red light on traffic light goes on. Green button, green light. Yellow button, yellow light. Blue button, all lights. This works great. 
2. Have a game of Simon. This also works great as a hunk of code by itself. 

I want to switch between the two modes above if a "mode" button is pressed on the controller. Pretty simple.
