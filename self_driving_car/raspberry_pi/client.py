import socket
import cv2
import struct
import pickle
import numpy as np
 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.0.18', 8485))
steering_value = b''
 
cap = cv2.VideoCapture(0)
 
# cap.set(3, 480);
# cap.set(4, 240);
 
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]
 
while True:
    ret, frame = cap.read()
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    data = np.array(frame)
    stringData = data.tostring()
 
    client.sendall((str(len(stringData))).encode().ljust(16) + stringData)
    steering_value = client.recv(10)
    steering_value = struct.unpack('f',steering_value)[0])
 
cap.release()
