#!/usr/bin/env python3
import cv2
from ClassCamera import ClassCamera
camera = ClassCamera()
camera.connect(0)
while True:
    camera.getData()
    cv2.imshow("preview", camera.image)
    key = cv2.waitKey(20)
    if key == 113:  # exit on "q"
        break

cv2.destroyWindow("preview")
camera.disconnect()