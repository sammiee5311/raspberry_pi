import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

class Motor():
    def __init__(self, right_power, left_power, right_forw, right_back, left_forw, left_back):
        self.right_power = right_power
        self.left_power = left_power
        self.right_forw = right_forw
        self.right_back = right_back
        self.left_forw = left_forw
        self.left_back = left_back
        gpio.setup(self.right_power, gpio.OUT)
        gpio.setup(self.left_power, gpio.OUT)
        gpio.setup(self.right_forw, gpio.OUT)
        gpio.setup(self.right_back, gpio.OUT)
        gpio.setup(self.left_forw, gpio.OUT)
        gpio.setup(self.left_back, gpio.OUT)
        self.left_pwm = gpio.PWM(self.left_power, 300)
        self.left_pwm.start(0)
        self.right_pwm = gpio.PWM(self.right_power, 300)
        self.right_pwm.start(0)

    def move(self, speed=0.5, turn=0, t=0):
        speed *= 100
        turn *= 100
        left_speed = speed-turn
        right_speed = speed+turn
        if left_speed > 100:
            left_speed = 100
        elif left_speed < -100:
            left_speed = -100
        if right_speed > 100:
            right_speed = 100
        elif right_speed < -100:
            right_speed = -100
        self.left_pwm.ChangeDutyCycle(abs(left_speed))
        self.right_pwm.ChangeDutyCycle(abs(right_speed))
        if right_speed > 0:
            gpio.output(self.right_forw, gpio.HIGH)
            gpio.output(self.right_back, gpio.LOW)
        else:
            gpio.output(self.right_forw, gpio.LOW)
            gpio.output(self.right_back, gpio.HIGH)
        if left_speed > 0:
            gpio.output(self.left_forw, gpio.HIGH)
            gpio.output(self.left_back, gpio.LOW)
        else:
            gpio.output(self.left_forw, gpio.LOW)
            gpio.output(self.left_back, gpio.HIGH)
        time.sleep(t)


def main():
    move()

if __name__ == '__main__':
    motor = Motor(5, 6, 27, 17, 22, 23)
    main()