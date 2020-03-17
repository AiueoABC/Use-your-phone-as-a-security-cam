import subprocess
import cv2
import sys
import socket
import time
import numpy as np

host_name = "192.168.0.80"  # destination
port_name = 16384
max_length = 10000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host_name, port_name))  # connection as client
while True:
    try:
        subprocess.call(["termux-camera-photo", "test1.png"])
        img = cv2.imread("./test1.png")
        sock.sendall(img.tobytes())
        time.sleep(0.1)
        sock.send(b'__end__')
        while True:
            buf = sock.recv(1024)
            print(buf)
            if b'break' in buf:
                break
            elif b'givemesize' in buf:
                sock.sendall(np.asarray(img.shape[:3]).tobytes())
    except Exception as e:
        print(e)
        break
try:
    sock.close()
except:
    pass
