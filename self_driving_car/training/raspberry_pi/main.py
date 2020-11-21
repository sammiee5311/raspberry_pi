from motor_module import Motor
import controller as ct
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
    Flag = True
    print("start")
    while True:
        _, image = cap.read()
        ct_val = ct.getJS()
        value = 0
        base_value = {0 : 0, 1 : 0.105, 2 : 0.11, 3 : 0.12, -1 : -0.105, -2 : -0.11, -3: -0.12}
        steering = ct_val['axis1']*0.13
        throttle = ct_val['o']*0.11
        
        if 0.09 < steering <= 0.10:
            value = 1
        elif 0.10 < steering <= 0.11:
            value = 2
        elif 0.12 < steering:
            value = 3
        elif -0.10 <= steering <= -0.09:
            value = -1
        elif -0.11 <= steering < -0.10:
            value = -2
        elif steering <= -0.12 :
            value = -3
        else:
            value = 0
            
        motor.move(throttle,-base_value[value])
        if not Flag:   
            X.append(image)
            y.append(value)
            cnt += 1
            
        if ct_val['x']:
            if Flag:
                Flag = False
            else:
                Flag = True
                
        if ct_val['s']:
            break
        cv2.waitKey(1)
        
    cnt = 0
    img_name = []
    for i in range(len(X)):
        img_name.append(cnt)
        cv2.imwrite(path+str(i)+'.jpg',X[i])
        cnt += 1

    df = pd.DataFrame({'img' : img_name, 'steering' : y})
    df.to_csv('save.csv')

if __name__ == '__main__':
    while True:
        main()
        break


