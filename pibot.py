#!/usr/bin/python3

import signal, sys, random
import RPi.GPIO as GPIO
from time import *
from subprocess import call


DEBUG = True

if DEBUG != True:
    GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

TRIG = 24
ECHO = 23
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
leftforward    = GPIO.PWM(27, 50)
rightbackward  = GPIO.PWM(17, 50)
rightforward   = GPIO.PWM(18, 50)
leftbackward   = GPIO.PWM(22, 50)


def range():
    GPIO.output(TRIG, False)
    sleep(1.5)

    GPIO.output(TRIG, True)
    sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time()
    while GPIO.input(ECHO) ==1:
        pulse_end = time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    if DEBUG:
        print(distance)
    return distance

def stop():
    leftforward.stop()
    rightforward.stop()
    leftbackward.stop()
    rightbackward.stop()
    sleep(0.05)

def forward(speed, time):
    leftforward.start(speed)
    rightforward.start(speed)
    sleep(time)
    stop()

def backward(speed, time):
    leftbackward.start(speed)
    rightbackward.start(speed)
    sleep(time)
    stop()


def turnleft(speed, time):
    leftbackward.start(speed)
    rightforward.start(speed)
    sleep(time)
    stop()



def turnright(speed, time):
    rightbackward.start(speed)
    leftforward.start(speed)
    sleep(time)
    stop()

    
def avoid():
    backward(70, 0.3)
    dir = random.choice(['l','r'])
    amount = random.randint(2, 10)
    amount = amount / 10.0
    if dir == 'r':
        turnright(70, amount)
    elif dir == 'l':
        turnleft(70, amount)
    else:
        print('eh?')

def go(speed):
    if (range() > 40):
        forward(speed, 0.5)
    else:
        avoid()

if __name__ == "__main__":
    print("press cntl-c to stop")
    while True: 
        try:
            go(80)
        except KeyboardInterrupt:
            print("\nkeyboard interrupt")
            GPIO.cleanup()
            sys.exit()
        except:
            print("Couldn't go")
            GPIO.cleanup()
            sys.exit()
    GPIO.cleanup()
    sys.exit()        

