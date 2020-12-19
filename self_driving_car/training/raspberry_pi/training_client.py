import socket
import cv2
import struct
import pickle

IP = ''
PORT = 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

try:
    cap = cv2.VideoCapture(0)
    while True:
        _, image = cap.read()
        data = pickle.dumps(image)
        img_data = struct.pack('L', len(data))
        client_socket.sendall(img_data+data)

except Exception as e:
    print("General error", str(e))
    client_socket.close()



