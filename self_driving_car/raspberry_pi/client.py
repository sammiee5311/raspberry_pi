import socket
import cv2
import struct
import pickle
import numpy as np
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.0.18', 8485))
steering_value = b''
 
cam = cv2.VideoCapture(0)
 
cam.set(3, 480);
cam.set(4, 240);
 
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
 
while True:
    ret, frame = cam.read()
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    data = np.array(frame)
    stringData = data.tostring()
 
    s.sendall((str(len(stringData))).encode().ljust(16) + stringData)
    steering_value = s.recv(10)
    print(struct.unpack('B',steering_value)[0])
 
cam.release()
