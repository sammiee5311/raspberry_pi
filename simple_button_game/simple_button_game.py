from gpiozero import LED, Button
from time import sleep
import random


class simple_button_game:
    def __init__(self):
        self.led1 = LED(17)
        self.led2 = LED(18)
        self.led3 = LED(22)
        self.led4 = LED(23)

        self.button1 = Button(26)
        self.button2 = Button(16)
        self.button3 = Button(21)
        self.button4 = Button(20)
        self.led_list = [self.led1, self.led2, self.led3, self.led4]
        self.stage = 1
        self.cnt_button = 1
        print('################START##################')

    def correct(self):
        for led in self.led_list:
            led.on()
        sleep(1)
        for led in self.led_list:
            led.off()
        sleep(1)

    def wrong(self):
        for led in self.led_list:
            led.on()
            sleep(0.5)
        for led in self.led_list:
            led.off()
            sleep(0.5)

    def normal(self, time=1, max_stage=10):
        while self.stage < max_stage:
            led_save = []
            button_save = []
            for _ in range(self.stage):
                led = random.choice(self.led_list)
                led.on()
                sleep(time)
                led.off()
                sleep(time)
                led_save.append(led)

            while self.cnt_button > 0:
                flag = False
                if self.button1.is_pressed:
                    button_save.append(self.led1)
                    flag = True
                    sleep(0.9)
                if self.button2.is_pressed:
                    button_save.append(self.led2)
                    flag = True
                    sleep(0.9)
                if self.button3.is_pressed:
                    button_save.append(self.led3)
                    flag = True
                    sleep(0.9)
                if self.button4.is_pressed:
                    button_save.append(self.led4)
                    flag = True
                    sleep(0.9)
                if flag is True:
                    self.cnt_button -= 1
                    continue

            if led_save == button_save:
                self.correct()

            elif led_save != button_save:
                self.wrong()
                exit()

            self.stage += 1
            self.cnt_button = self.stage
            sleep(0.1)


game = simple_button_game()
# choose the time (how long the light will be stayed on) & max_stage
# default time is 1 second, max_stage is 10 stages
game.normal(time=1, max_stage=10)
