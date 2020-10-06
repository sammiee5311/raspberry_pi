import socket
import pickle
import cv2
import numpy as np
import struct
from keras.models import load_model


IP = '127.0.0.1'
PORT = 15946
model = load_model('my_model.h5')

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()
print("waiting for connection")

connection, address = server_socket.accept()

try:
    bytes = b''
    bytes += connection.recv(1024)
    payload_size = struct.calcsize("L")
    while True:
        while len(bytes) < payload_size:
            bytes += connection.recv(1024)
        packed_msg_size = bytes[:payload_size]
        bytes = bytes[payload_size:]
        msg_size = struct.unpack('L', packed_msg_size)[0]

        while len(bytes) < msg_size:
            bytes += connection.recv(1024)
        frame_data = bytes[:msg_size]
        bytes = bytes[msg_size:]

        frame = pickle.loads(frame_data)

        image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        height,width = image.shape
        roi = image[height // 2:height, :]
        roi /= 2555
        roi = np.array([roi])
        steering_value = float(model.predict(roi))
        connection.send(struct.pack('B', steering_value))
        cv2.imshow('frame', roi)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    try:
        pass
    except IOError as e:
        print(e)

finally:
    connection.close()
    server_socket.close()
