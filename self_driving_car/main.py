from setup import Motor
import key as kp

motor = Motor(5, 6, 27, 17, 23, 22)
kp.init()


def main():
    if kp.get_key('UP'):
        motor.move(0.7,0,0.1)
    elif kp.get_key('DOWN'):
        motor.move(-0.7,0,0.1)
    elif kp.get_key('LEFT'):
        motor.move(0.5,-0.3,0.1)
    elif kp.get_key('RIGHT'):
        motor.move(0.5,0.3,0.1)
    else:
        motor.stop(0.1)
if __name__ == '__main__':
    while True:
        main()