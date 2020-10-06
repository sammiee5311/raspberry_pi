import socket
import cv2
import struct
import pickle

IP = '127.0.0.1'
PORT = 15946

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

try:
    cap = cv2.VideoCapture('test.mp4')
    while True:
        cnt += 1
        _, image = cap.read()
        data = pickle.dumps(image)
        message_size = struct.pack('L', len(data))
        client_socket.sendall(message_size+data)

except Exception as e:
    print("General error", str(e))
    client_socket.close()



