#!/usr/bin/python3
from pibotmotors import PibotMotors
from pibotsensors import PibotSensors
import time
import atexit
import sys

class Pibot(PibotSensors, PibotMotors):
    def __init__(self):
        PibotSensors.__init__(self)
        PibotMotors.__init__(self)

    def forward(self, speed, seconds=None):
        """Move forward at the specified speed (0-255).  Will start moving
        forward and return unless a seconds value is specified, in which
        case the robot will move forward for that amount of time and then stop.

        Over-rides similar method in PibotMotors to add functionality of sensing
        whether way ahead is clear.
        """
        # Set motor speed and move both forward.
        
        self._right_speed(speed)
        self._left_speed(speed)
        
        # If an amount of time is specified, move for that time and then stop.
        if seconds is None:
            for motor in self._motors:
                motor.run(self.FORWARD)
            while (robot.frontLeftClear and robot.frontRightClear):
                time.sleep(0.1)
            self.stop()
        else:
            for motor in self._motors:
                motor.run(self.FORWARD)
            time.sleep(seconds)
            self.stop()



if __name__ == "__main__":
    print("press cntl-c to stop")
    robot = Pibot()
    while True: 
        try:
            robot.forward(150)
            robot.stop
            sys.exit()

        except KeyboardInterrupt:
            print("\nkeyboard interrupt")
            sys.exit()
#        except:
#            print("Couldn't go")
#            sys.exit()
    sys.exit()  
