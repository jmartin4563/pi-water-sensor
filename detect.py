#!/usr/bin/python

import RPi.GPIO as GPIO
from sparkpost import SparkPost
import time
import os

sparkpostKey = os.environ.get('SPKEY')
twilioKey = os.environ.get('TWILIOKEY')
sparky = SparkPost(sparkpostKey)

# Yay, you don't have water anymore
def sendHappyEmail():
    sparkySays = sparky.transmissions.send(
        recipients=['jessica.martin@sparkpost.com'],
        template='detector-email-happy'
    )

# Boo, you have water detected
def sendSadEmail():
    sparkySays = sparky.transmissions.send(
        recipients=['jessica.martin@sparkpost.com'],
        template='detector-email-sad'
    )

# Generic callback handler for any state change
def inputCallback(channel):
    if GPIO.input(channel):
        print('No Water Detected')
        sendHappyEmail()
    else:
        print('Water Detected')
        sendSadEmail()

# Setup the pin we are listening to
GPIO.setmode(GPIO.BOARD)
channel = 38
GPIO.setup(channel, GPIO.IN)

# Add our event handlers and callback (bouncetime is for preventing false positive changes
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=1000)
GPIO.add_event_callback(channel, inputCallback)

# Infinite loop of detection, with a sleep to keep CPU down on the Pi
while True:
    time.sleep(0.5)

