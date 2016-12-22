import RPi.GPIO as GPIO
import threading
from time import sleep, time

class PibotSensors(object):
    def __init__(self):
        # initialise GPIO for corner sensoring
        self.frontLeftClear = None
        self.frontRightClear = None
        self.frontLeftPin = 19
        self.frontRightPin = 16
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.frontLeftPin, GPIO.IN) 
        GPIO.setup(self.frontRightPin, GPIO.IN)
        self.stopEvent = None
        self.CornerSensorsThread = None

        # initialise GPIO for distance sensoring
        self.distanceAhead = None
        self.DistanceSensorsThread = None
        self.trigPin = 21
        self.echoPin = 20
        GPIO.setup(self.trigPin, GPIO.OUT)
        GPIO.output(self.trigPin, False)
        GPIO.setup(self.echoPin, GPIO.IN)
        
        # start a thread that constantly polls the corner sensors
        self.stopEvent = threading.Event()
        self.CornerSensorsThread = threading.Thread(target=self.checkClear, 
                                                    args=())
        self.CornerSensorsThread.start()

        # start a thread that constantly polls the distance sensor
        self.DistanceSensorsThread = threading.Thread(target=self.checkDistance,
                                                      args=())
        self.DistanceSensorsThread.start()

    def checkClear(self):
        while not self.stopEvent.is_set():
            self.frontLeftClear = GPIO.input(self.frontLeftPin)
            self.frontRightClear = GPIO.input(self.frontRightPin)

    def checkDistance(self):
        while not self.stopEvent.is_set():
            sleep(2)
            GPIO.output(self.trigPin, True)
            sleep(0.00001)
            GPIO.output(self.trigPin, False)
            while False == GPIO.input(self.echoPin):
                pulse_start = time()
            while True == GPIO.input(self.echoPin):
                pulse_end = time()
            pulse_duration = pulse_end - pulse_start
            self.distanceAhead = round(pulse_duration * 17150, 2)

    def onClose(self): 
        self.stopEvent.set()
        GPIO.output(self.trigPin, False)

if __name__ == "__main__":
    print("press cntl-c to stop")
    sensors = PibotSensors()
    while True:
        try:
            if (True == sensors.frontRightClear):
                frontRight = "clear"
            elif (False == sensors.frontRightClear):
                frontRight = "obstructed"
            elif (None == sensors.frontRightClear):
                frontRight = "not working"
            else: 
                raise("error front right sensor")

            if (True == sensors.frontLeftClear):
                frontLeft = "clear"
            elif (False == sensors.frontLeftClear):
                frontLeft = "obstructed"
            elif (None == sensors.frontLeftClear):
                frontLeft = "not working"
            else: 
                raise("error front left sensor")

            print("Front right is %s. Front left is %s" % 
                     (frontRight, frontLeft) )
            print("Dstance ahead is %s" % (sensors.distanceAhead) )
        except KeyboardInterrupt:
            print("\nkeyboard interrupt")
            sys.exit()
        except:
            print("something went wrong")
        sleep(1)


