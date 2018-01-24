import socket as s
import struct
import numpy as np
import yolo
import cv2
from datetime import datetime

port = 4444

serversocket = s.socket()
serversocket.bind((s.gethostname(), port))
serversocket.listen()

def udp_thread():
    udp_sock = s.socket(s.AF_INET, s.SOCK_DGRAM)
    udp_sock.bind((s.gethostname(),4445))
    print('Waiting for udp ping!')
    while True:
        msg, addr = udp_sock.recvfrom(256)
        print('Recieved udp ping from {}!'.format(addr))
        udp_sock.sendto(msg, addr)

def debug_thread():
    debug_serversock = s.socket()
    debug_serversock.bind((s.gethostname(), 4443))
    
    debug_sock, addr = debug_serversock.accept()
    while True:
        msg_len = recieve_int(debug_sock)
        msg = recieve(msg_len)
        print('Debug: {} - {}'.format(now(), msg.decode('utf-8')))

def now():
    return datetime.now().strftime('%m-%d-%Y %I:%M %p')

"""
thread = threading.Thread(target = udp_thread, args=())
thread.daemon = True
thread.start()
"""

input('Press enter to start server...')
print('Started!')

print('Waiting for TCP connection...')
socket, addr = serversocket.accept()
print('Recieved TCP connection from {}!'.format(addr))

def recieve(socket, msg_len):
    chunks = []
    bytes_recd = 0
    while bytes_recd < msg_len:
        chunk = socket.recv(min(msg_len - bytes_recd, 2048))
        if chunk == b'':
            raise RuntimeError("socket connection broken")
        chunks.append(chunk)
        bytes_recd = bytes_recd + len(chunk)
    return b''.join(chunks)

def recieve_int(socket):
    return struct.unpack('!i', recieve(socket, 4))[0]

def bytes_to_img(data, width, height, n_channels):
    global img, x, y
    img = np.empty((height, width, n_channels), dtype=np.uint8)
    for i in range(0, len(data), n_channels):
        x =int((i/n_channels) % width)
        y = int((i/n_channels) // width)
        global s
        s = data[i:i+n_channels]
        s = [int(i) for i in s]
        img[y,x] = np.array(s)
    return img

def clamp(num, low, high):
    return min(max(num,low),high)

from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'auto')
del get_ipython

while True:
    # Recieve image dimensions
    global img_width, img_height, img_data
    img_width = recieve_int(socket)
    img_height = recieve_int(socket)
    if not (img_width == img_height == 416):
        print('Bad size: {}x{}'.format(img_width, img_height))
        
    
    # Recieve image bytes and convert to np array
    n_channels = recieve_int(socket)
    global img_data
    raw_data = recieve(socket, img_width*img_height*n_channels)
    img_data = bytes_to_img(raw_data, img_width, img_height, n_channels)
    drawn_img = yolo.draw_pred(img_data)
    cv2.imshow('Robot', np.asarray(drawn_img))