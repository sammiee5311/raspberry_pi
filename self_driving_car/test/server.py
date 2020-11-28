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


model = load_model('')
IP = ''
PORT = 

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("waiting for connection")

server_socket.bind((IP, PORT))
server_socket.listen(1)

values = {0 : 0.12, 1 : 0.13, 2 : 0.135, 3 : 0, 4: -0.12, 5 : -0.13, 6 : -0.135}

connection, address = server_socket.accept()

while True:
    length = recvall(connection, 16)
    stringData = recvall(connection, int(length))
    data = np.frombuffer(stringData, dtype='uint8')
    frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2YUV)
    frame = cv2.GaussianBlur(frame,  (3, 3), 0)
    h, w, _ = frame.shape
    roi = frame[int(h / 2):h, :, :]
    roi = np.asarray(roi)
    roi = roi.astype('float32')
    roi = roi / 225.
    roi = np.array([roi])
    if len(roi.shape) == 4:
        steering_value = model.predict(roi)
        connection.send(struct.pack('f', values[steering_value[0].argmax()]))
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
