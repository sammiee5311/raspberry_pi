import socket
import cv2
import numpy as np
import struct
from keras.models import load_model


def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


model = load_model('my_model2.h5')
IP = '192.168.0.18'
PORT = 9484
input_size = 480*320

frame = cv2.imread('./training/Images/1916.jpg')

h, w, _ = frame.shape
roi = frame[int(h / 2):h, :, :]
roi = np.asarray(roi)
roi = roi / 225.
roi = np.array([roi])
steering_value = model.predict(roi)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("waiting for connection")

server_socket.bind((IP, PORT))
server_socket.listen(1)

connection, address = server_socket.accept()
# steering_value = 0

while True:
    length = recvall(connection, 16)
    stringData = recvall(connection, int(length))
    data = np.frombuffer(stringData, dtype='uint8')
    frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
    # cv2.imshow('img', frame)
    h, w, _ = frame.shape
    roi = frame[int(h / 2):h, :, :]
    roi = np.asarray(roi)
    roi = roi / 225.
    roi = np.array([roi])
    if len(roi.shape) == 4:
        steering_value = model.predict(roi)
        print(steering_value)
        connection.send(struct.pack('f', steering_value[0][0]))
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break