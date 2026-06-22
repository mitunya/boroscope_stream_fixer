import cv2
import time

# before execute bsf
# ./bsf -i tcp:192.168.10.123:7060 -o tcp::7060

cap = cv2.VideoCapture("http://localhost:7060")
while True:
    ret, frame = cap.read()
    cv2.imshow('Video', frame)
    # esc key
    if cv2.waitKey(1) == 27:
        exit(0)

# cv2 install : pip install open-python opencv-contrib-python

# Public License, free use.
