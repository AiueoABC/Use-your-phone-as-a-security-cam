import subprocess
import cv2
import sys
import socket
import time
import numpy as np

try:
    external_sending = int(sys.argv[1])
except:
    external_sending = 0
subprocess.call(["termux-camera-photo", "test.png"])
img = cv2.imread("./test.png")
if external_sending == 0:
    exit()
size = np.asarray(img.shape[:3])
host_name = "192.168.0.80" # destination
port_name = 16384
max_length = 10000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host_name, port_name))  # connection as client
bindata = img.tobytes()
binlength = bindata.__len__()
idx0 = 0
sock.sendall(bindata)
time.sleep(0.1)
sock.send(b'__end__')
while True:
    buf = sock.recv(1024)
    print(buf)
    if b'break' in buf:
        break
    elif b'givemesize' in buf:
        sock.sendall(size.tobytes())
sock.close()
