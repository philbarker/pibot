#!/usr/bin/python3
from Adafruit_MotorHAT import Adafruit_MotorHAT
import time
import atexit
import sys

class Motors(object):
    def __init__(self, addr=0x60, front_left_id=1, front_right_id=2, front_left_trim=0, front_right_trim=0,
                  rear_left_id=3, rear_right_id=4, rear_left_trim=0, rear_right_trim=0, stop_at_exit=True):

        """Create an instance of the robot.  Can specify the following optional
        parameters:
         - addr: The I2C address of the motor HAT, default is 0x60.
         - front_left_id: The ID of the left motor, default is 1.
         - front_right_id: The ID of the right motor, default is 2.
         - front_left_trim: Amount to offset the speed of the left motor, can be positive
                      or negative and use useful for matching the speed of both
                      motors.  Default is 0.
         - front_right_trim: Amount to offset the speed of the right motor (see above).
         - rear_left_id: The ID of the left motor, default is 3.
         - rear_right_id: The ID of the right motor, default is 4.
         - rear_left_trim: Amount to offset the speed of the left motor, can be positive
                      or negative and use useful for matching the speed of both
                      motors.  Default is 0.
         - rear_right_trim: Amount to offset the speed of the right motor (see above).
         - stop_at_exit: Boolean to indicate if the motors should stop on program
                         exit.  Default is True (highly recommended to keep this
                         value to prevent damage to the bot on program crash!).
        """
        # Initialize motor HAT and left, right motor.
        self._mh = Adafruit_MotorHAT(addr)
        self._front_left = self._mh.getMotor(front_left_id)
        self._front_right = self._mh.getMotor(front_right_id)
        self._front_left_trim = front_left_trim
        self._front_right_trim = front_right_trim
        self._rear_left = self._mh.getMotor(rear_left_id)
        self._rear_right = self._mh.getMotor(rear_right_id)
        self._rear_left_trim = rear_left_trim
        self._rear_right_trim = rear_right_trim
        self._left_motors = [self._front_left, self._rear_left]
        self._right_motors = [self._front_right, self._rear_right]
        self._motors = [self._front_left, self._front_right, self._rear_left, self._rear_right]
        # Start with motors turned off.
        self._front_left.run(Adafruit_MotorHAT.RELEASE)
        self._front_right.run(Adafruit_MotorHAT.RELEASE)
        self._rear_left.run(Adafruit_MotorHAT.RELEASE)
        self._rear_right.run(Adafruit_MotorHAT.RELEASE)
        # Configure all motors to stop at program exit if desired.
        if stop_at_exit:
            atexit.register(self.stop)

    def _left_speed(self, speed):
        """Set the speed of the left motor, taking into account its trim offset.
        """
        assert 0 <= speed <= 255, 'Speed must be a value between 0 to 255 inclusive!'
        front_speed = speed + self._front_left_trim
        rear_speed = speed + self._rear_left_trim
        front_speed = max(0, min(255, speed))  # Constrain speed to 0-255 after trimming.
        rear_speed = max(0, min(255, speed))  # Constrain speed to 0-255 after trimming.
        self._front_left.setSpeed(front_speed)
        self._rear_left.setSpeed(rear_speed)

    def _right_speed(self, speed):
        """Set the speed of the right motor, taking into account its trim offset.
        """
        assert 0 <= speed <= 255, 'Speed must be a value between 0 to 255 inclusive!'
        front_speed = speed + self._front_right_trim
        rear_speed = speed + self._rear_right_trim
        front_speed = max(0, min(255, speed))  # Constrain speed to 0-255 after trimming.
        rear_speed = max(0, min(255, speed))  # Constrain speed to 0-255 after trimming.
        self._front_right.setSpeed(front_speed)
        self._rear_right.setSpeed(rear_speed)

    def stop(self):
        """Stop all movement."""
        for motor in self._motors:
            motor.run(Adafruit_MotorHAT.RELEASE)


    def forward(self, speed, seconds=None):
        """Move forward at the specified speed (0-255).  Will start moving
        forward and return unless a seconds value is specified, in which
        case the robot will move forward for that amount of time and then stop.
        """
        # Set motor speed and move both forward.
        self._right_speed(speed)
        self._left_speed(speed)
        for motor in self._motors:
            motor.run(Adafruit_MotorHAT.FORWARD)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

    def backward(self, speed, seconds=None):
        """Move backward at the specified speed (0-255).  Will start moving
        backward and return unless a seconds value is specified, in which
        case the robot will move backward for that amount of time and then stop.
        """
        # Set motor speed and move both backward.
        self._right_speed(speed)
        self._left_speed(speed)
        for motor in self._motors:
            motor.run(Adafruit_MotorHAT.BACKWARD)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

    def right(self, speed, seconds=None):
        """Spin to the right at the specified speed.  Will start spinning and
        return unless a seconds value is specified, in which case the robot will
        spin for that amount of time and then stop.
        """
        # Set motor speed and move both forward.
        self._left_speed(speed)
        self._right_speed(speed)
        for motor in self._left_motors:
            motor.run(Adafruit_MotorHAT.FORWARD)
        for motor in self._right_motors:
            motor.run(Adafruit_MotorHAT.BACKWARD)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

    def left(self, speed, seconds=None):
        """Spin to the left at the specified speed.  Will start spinning and
        return unless a seconds value is specified, in which case the robot will
        spin for that amount of time and then stop.
        """
        # Set motor speed and move both forward.
        self._left_speed(speed)
        self._right_speed(speed)
        for motor in self._left_motors:
            motor.run(Adafruit_MotorHAT.BACKWARD)
        for motor in self._right_motors:
            motor.run(Adafruit_MotorHAT.FORWARD)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

if __name__ == "__main__":
    print("press cntl-c to stop")
    motors = Motors()


    # test 1. slow forward 1 second
    print('test 1. slow forward 1 second')
    try:
        motors.forward(80,1)
    except KeyboardInterrupt:
        print("\nkeyboard interrupt")
        sys.exit()
    except:
        print("Couldn't go")
        sys.exit()
    time.sleep(1)

    #unit test 2. slow forward 3 second
    print('test 2. slow forward 3 second')
    try:
        motors.forward(80,3)
    except KeyboardInterrupt:
        print("\nkeyboard interrupt")
        sys.exit()
    except:
        print("Couldn't go")
        sys.exit()
    time.sleep(1)

    #unit test 3. fast forward 1 second
    print('test 3. fast forward 1 second')
    try:
        motors.forward(200,1)
    except KeyboardInterrupt:
        print("\nkeyboard interrupt")
        sys.exit()
    except:
        print("Couldn't go")
        sys.exit()
    time.sleep(1)

    #unit test 4. fast forward 2 second
    print('test 4. fast backward 2 second')
    try:
        motors.backward(200,2)
    except KeyboardInterrupt:
        print("\nkeyboard interrupt")
        sys.exit()
    except:
        print("Couldn't go")
        sys.exit()
    time.sleep(1)


    sys.exit()  
