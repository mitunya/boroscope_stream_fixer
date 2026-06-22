frame_start = bytearray(b'BoundaryS') # [ b'B', b'o', b'u', b'n', b'd', b'a', b'r', b'y', b'S' ]
frame_end = [ b'B', b'o', b'u', b'n', b'd', b'a', b'r', b'y', b'E' ]
frame_start_len = len(frame_start)

"""
struct __attribute__((__packed__)) frame_header
{
    u_int8_t p1;
    u_int8_t p2;
    u_int8_t p3;
    u_int8_t p4;
    u_int32_t size;
    u_int32_t p6;
    u_int32_t p7;
    u_int32_t p8;
    u_int16_t p9;
    u_int16_t p10;
    u_int32_t width;
    u_int32_t height;
};
bbbbIIIHHII
"""

import sys
import datetime
import socket
import struct
import math
import numpy as np
import cv2

frame_header_fmt = '<bbbbIIIIHHII'
frame_header_length = struct.calcsize(frame_header_fmt)
print(frame_header_length)
buf_frame_header = bytearray(frame_header_length)

key_quit = [ord('q'), ord('Q'), ord(b'\x1b')]

host = '192.168.10.123'
port = 7060

sock = socket.socket()
sock.connect((host, port))

image_buffer = bytearray(256 * 1024)

matching_index = 0
while True:
    ch = sock.recv(1)
    if ord(ch) == frame_start[matching_index]:
        matching_index += 1

        if matching_index == frame_start_len:
            buf_frame_header = bytearray(sock.recv(frame_header_length))
            frame_header = struct.unpack(frame_header_fmt, buf_frame_header)

            frame_size = frame_header[4]

            #image_buffer = bytearray(frame_size)
            sock.recv_into(image_buffer, frame_size)

            image_buffer[math.floor(frame_size / 2)] = image_buffer[math.floor(frame_size / 2)] ^ 0xff
            image = cv2.imdecode(np.frombuffer(image_buffer[:frame_size], dtype=np.uint8), cv2.IMREAD_COLOR)

            try:
                cv2.imshow('host',image)
                k = cv2.waitKey(int(1000/15)) & 0xff
                if k in key_quit:
                    break
            except Exception as e:
                print('drop')
                pass

            print(datetime.datetime.now())
            sock.recv_into(buf_frame_header, len(frame_end))

            matching_index = 0
    else:
        matching_index = 0

sock.close()
