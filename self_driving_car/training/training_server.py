import socket
import pickle
import cv2
import numpy as np
import struct
import pandas

IP = '127.0.0.1'
PORT = 15946

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()
print("waiting for connection")

connection, address = server_socket.accept()

cnt = 0
steering_value = 0

X = []
y = []

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
        connection.send(struct.pack('B', cnt))

        image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        height,width = image.shape
        roi = image[height // 2:height, :]
        cv2.imshow('frame', roi)
        X.append(roi)
        y.append(steering_value)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    try:
        for img in X:
            cnt += 1
            cv2.imwrite(str(cnt)+'.jpg')
        df = pd.dataFrame({'img' : X, 'steering_value': y})
        df.to_csv('model.csv')
    except IOError as e:
        print(e)

finally:
    connection.close()
    server_socket.close()
