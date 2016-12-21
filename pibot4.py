#!/usr/bin/python3
from pibotmotors import Motors
import time
import atexit
import sys


if __name__ == "__main__":
    print("press cntl-c to stop")
    robot = Motors()
    while True: 
        try:
            robot.forward(80,1)
        except KeyboardInterrupt:
            print("\nkeyboard interrupt")
            sys.exit()
#        except:
#            print("Couldn't go")
#            sys.exit()
    sys.exit()  
