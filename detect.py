#!/usr/bin/python

import RPi.GPIO as GPIO
from sparkpost import SparkPost
from twilio.rest import Client
import time
import os

# Connection Setup for SP and Twilio
sparkpostKey = os.environ.get('SPKEY')
twilioKey = os.environ.get('TWILIOKEY')
twilioAccount = os.environ.get('TWILIOACCT')
sparky = SparkPost(sparkpostKey)
twilio = Client(twilioAccount, twilioKey)


# Yay, you don't have water anymore
def sendHappyEmail():
    sparky.transmissions.send(
        recipients=['jessica.martin@sparkpost.com'],
        template='detector-email-happy'
    )

def sendHappyText():
    twilio.messages.create(
        to='+14436059355',
        from_='+14438927539',
        body='Hooray! No more water in your basement'
    )

# Boo, you have water detected
def sendSadEmail():
    sparky.transmissions.send(
        recipients=['jessica.martin@sparkpost.com'],
        template='detector-email-sad'
    )

def sendSadText():
    twilio.messages.create(
        to='+14436059355',
        from_='+14438927539',
        body='Uh oh! We have detected that there is water in your basement'
    )

# Generic callback handler for any state change
def inputCallback(channel):
    if GPIO.input(channel):
        print('No Water Detected')
        sendHappyEmail()
        sendHappyText()
    else:
        print('Water Detected')
        sendSadEmail()
        sendSadText()

# Setup the pin we are listening to
GPIO.setmode(GPIO.BOARD)
channel = 38
GPIO.setup(channel, GPIO.IN)

# Add our event handlers and callback (bouncetime is for preventing false positive changes)
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=1000)
GPIO.add_event_callback(channel, inputCallback)

# Infinite loop of detection, with a sleep to keep CPU down on the Pi
while True:
    time.sleep(0.5)

