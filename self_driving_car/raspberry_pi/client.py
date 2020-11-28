import socket
import RPi.GPIO as GPIO
import cv2
import struct
import numpy as np

########################################
from motor_module import Motor
from ultrasonic_module import Ultrasonic
########################################

GPIO.cleanup()
IP = ''
PORT = 

motor = Motor(5, 27, 17, 6, 23, 22)
dis = Ultrasonic()
dis.set_GPIO()
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))

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
    steering_value = struct.unpack('f',steering_value)[0
                                                       
    distance = dis.get_distance()
    if distance <= 10:
        motor.move(0,0)
    else:
        motor.move(0.11,steering_value)

cam.release()
