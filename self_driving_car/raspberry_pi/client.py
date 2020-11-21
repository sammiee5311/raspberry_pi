import socket
import cv2
import struct
import pickle
import numpy as np
from motor_module import Motor

motor = Motor(5, 27, 17, 6, 23, 22)
IP =  
PORT = 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('IP', PORT))
steering_value = b''
 
cam = cv2.VideoCapture(0)
 
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]
 
while True:
    ret, frame = cam.read()
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    data = np.array(frame)
    stringData = data.tostring()
 
    s.sendall((str(len(stringData))).encode().ljust(16) + stringData)
    steering_value = s.recv(10)
    steering_value = struct.unpack('f',steering_value)[0]
    motor.move(0.12,steering_value)
 
cam.release()

