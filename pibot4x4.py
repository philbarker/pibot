#!/usr/bin/python3
from time import sleep
import atexit, sys
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

motors = (mh.getMotor(1), mh.getMotor(2),mh.getMotor(3), mh.getMotor(4))
rmotors = (mh.getMotor(2), mh.getMotor(4))
lmotors = (mh.getMotor(1), mh.getMotor(3))

def stop():
    for motor in motors:
        motor.setSpeed(0)

def forward(speed = 126, duration = 1):
    for motor in motors:
        motor.setSpeed(speed)
        motor.run(Adafruit_MotorHAT.FORWARD)
    sleep(duration)
    stop()

def veerright(speed = 126, duration = 1):
    for motor in rmotors:
        motor.setSpeed(speed//2)
        motor.run(Adafruit_MotorHAT.FORWARD)
    for motor in lmotors:
        motor.setSpeed(speed)
        motor.run(Adafruit_MotorHAT.FORWARD)
    sleep(duration)
    stop()

def veerleft(speed = 126, duration = 1):
    for motor in lmotors:
        motor.setSpeed(speed//2)
        motor.run(Adafruit_MotorHAT.FORWARD)
    for motor in rmotors:
        motor.setSpeed(speed)
        motor.run(Adafruit_MotorHAT.FORWARD)
    sleep(duration)
    stop()


def turnright(speed = 126, duration = 1):
    for motor in rmotors:
        motor.setSpeed(speed)
        motor.run(Adafruit_MotorHAT.BACKWARD)
    for motor in lmotors:
        motor.setSpeed(speed)
        motor.run(Adafruit_MotorHAT.FORWARD)
    sleep(duration)
    stop()

def turnleft(speed = 126, duration = 1):
    for motor in lmotors:
        motor.setSpeed(speed)
        motor.run(Adafruit_MotorHAT.BACKWARD)
    for motor in rmotors:
        motor.setSpeed(speed)
        motor.run(Adafruit_MotorHAT.FORWARD)
    sleep(duration)
    stop()


def backward(speed = 126, duration = 1):
    for motor in motors:
        motor.setSpeed(speed)
        motor.run(Adafruit_MotorHAT.BACKWARD)
    sleep(duration)
    stop()


if __name__ == "__main__":
    forward(255, 1)
    backward(255, 1)
    turnright(126,1)
    turnleft(126,1)
    turnOffMotors()
    sys.exit

