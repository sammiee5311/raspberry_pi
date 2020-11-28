import RPi.GPIO as GPIO
import time


class Ultrasonic:
    def __init__(self):
        self.TRIG = 4
        self.ECHO = 24
        self.MAX_DISTANCE = 300
        self.MAX_TIMEOUT = (self.MAX_DISTANCE * 2 * 29.1)

    def set_GPIO(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)
        GPIO.output(self.TRIG, False)

    def get_distance(self):
            
        GPIO.output(self.TRIG, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, False)

        timeout = time.time()
        while GPIO.input(self.ECHO) == 0:
            pulse_start = time.time()
            if ((pulse_start - timeout)*1000000) >= self.MAX_TIMEOUT:
                break

        timeout = time.time()
        while GPIO.input(self.ECHO) == 1:
            pulse_end = time.time()
            if ((pulse_end - pulse_start)*1000000) >= self.MAX_TIMEOUT:
                break

        pulse_duration = (pulse_end - pulse_start) * 1000000
        distance = (pulse_duration / 2) / 29.1
        
        return int(distance)


if __name__ == '__main__':
    a = Ultrasonic()
    a.set_GPIO()
    b = a.get_distance()
    GPIO.cleanup()

