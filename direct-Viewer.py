'''
https://dev.to/linou518/when-macos-26-tahoe-blocked-python-socket-connections-and-how-launchdaemon-fixed-it-3j2i

https://mkarr.github.io/20200616_boroscope

need sudo
'''

def hex_dump(data, length=16):
    """ Dump Hex decimal """
    for i in range(0, len(data), length):
        chunk = data[i:i+length]
        hex_part = ' '.join(f'{byte:02x}' for byte in chunk)
        ascii_part = ''.join(chr(byte) if 32 <= byte < 127 else '.' for byte in chunk)
        print(f'{i:04x}  {hex_part:<{length*3}}  {ascii_part}')


frame_boundary_start = bytearray(b'BoundaryS') # [ b'B', b'o', b'u', b'n', b'd', b'a', b'r', b'y', b'S' ]
frame_boundary_start_len = len(frame_boundary_start)
frame_boundary_end = bytearray(b'BoundaryE') # [ b'B', b'o', b'u', b'n', b'd', b'a', b'r', b'y', b'E' ]
frame_boundary_end_len = len(frame_boundary_end)
dummy = bytearray(frame_boundary_start_len)

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
buf_frame_header = bytearray(frame_header_length)

key_quit = [ord('q'), ord('Q'), ord(b'\x1b')]

host = '192.168.10.123'
port = 7060

sock = socket.socket()
sock.connect((host, port))

image_buffer = bytearray(256 * 1024)

matching_index = 0
drop = 0

while True:
    ch = sock.recv(1)
    if ord(ch) == frame_boundary_start[matching_index]:
        matching_index += 1

        if matching_index == frame_boundary_start_len:
            buf_frame_header = bytearray(sock.recv(frame_header_length))
            frame_header = struct.unpack(frame_header_fmt, buf_frame_header)
            frame_size = frame_header[4]

            sock.recv_into(image_buffer, frame_size)

            image_buffer[math.floor(frame_size / 2)] = image_buffer[math.floor(frame_size / 2)] ^ 0xff
            image = cv2.imdecode(np.frombuffer(image_buffer[:frame_size], dtype=np.uint8), cv2.IMREAD_COLOR)

            try:
                cv2.imshow('host',image)
                k = cv2.waitKey(int(1000/15)) & 0xff
                if k in key_quit:
                    break
                drop = 0
            except Exception as e:
                drop += 1
                print(datetime.datetime.now(), "frame drop:", drop)
                pass

            # print(datetime.datetime.now())
            sock.recv_into(buf_frame_header, frame_boundary_end_len)
            matching_index = 0
    else:
        matching_index = 0

sock.close()
