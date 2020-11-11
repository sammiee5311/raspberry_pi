from Motor_module import Motor
import Controller as ct
import pandas as pd
import cv2
import os
import numpy as np
from PIL import Image

motor = Motor(5, 27, 17, 6, 23, 22)
path = './Images/'


def main():
    cap = cv2.VideoCapture(0)
    X = []
    y = []
    cnt = 0
    maxThrottle = 0.25
    while True:
        _, image = cap.read()
        # image_cp = image.copy()
        # image_cp = cv2.cvtColor(image_cp,cv2.COLOR_RGB2GRAY)
        # height, width = image_cp.shape
        # roi = image_cp[int(height/2):height,:]
        # cv2.imshow('img',image)
        ct_val = ct.getJS()
        steering = ct_val['axis1']*0.4
        throttle = ct_val['o']*maxThrottle
        motor.move(throttle,-steering)
        X.append(image)
        y.append(str(round(steering,5)))
        cnt += 1
        print("steering : ", steering, "throttle : ", throttle)
        if ct_val['x']:
           break
        cv2.waitKey(1)
    cnt = 0
    img_name = []
    for i in range(len(X)):
        img_name.append(cnt)
        img = Image.fromarray(X[i])
        img.save(path+str(i)+'.jpg')
        cnt += 1

    df = pd.DataFrame({'img' : img_name, 'steering' : y})
    df.to_csv('save.csv')


if __name__ == '__main__':
    while True:
        main()
        break

