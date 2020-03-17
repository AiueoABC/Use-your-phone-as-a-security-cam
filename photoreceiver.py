import socket
from contextlib import closing
import numpy as np
import cv2

host_name = "192.168.0.80" # destination
port_name = 16384
buffer_size = 50000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
size = "0"
with closing(sock):
        sock.bind((host_name, port_name))
        sock.listen(1)
        while True:
            conn, addr = sock.accept()
            bin_data = bytes()
            while True:
                buf = conn.recv(buffer_size)
                if b'__end__' in buf:
                    conn.send(b'givemesize')
                    size_bin = conn.recv(buffer_size)
                    conn.send(b'break')
                    img = np.frombuffer(bin_data, dtype=np.uint8).reshape(np.frombuffer(size_bin, dtype=np.int))
                    print(np.frombuffer(size_bin, dtype=np.int))
                    break
                bin_data += buf
            cv2.imshow("test", cv2.resize(img, dsize=(600, 800)))
            cv2.waitKey(0)
            cv2.destroyAllWindows()

