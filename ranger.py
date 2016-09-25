#!/usr/bin/python

import RPi.GPIO as GPIO
from time import *

GPIO.setmode(GPIO.BCM)

TRIG = 24
ECHO = 23
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)


def range():
    print "distance measurement in progress"
    GPIO.output(TRIG, False)
    print "Waiting for sensor to settle"
    sleep(2)

    GPIO.output(TRIG, True)
    sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time()
    while GPIO.input(ECHO) ==1:
        pulse_end = time()
#        if pulse_end - pulse_start > 2:
#           break

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance


print "Distance: ", range(),"cm"

GPIO.cleanup()

