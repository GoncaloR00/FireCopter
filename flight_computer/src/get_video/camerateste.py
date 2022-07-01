#!/usr/bin/env python3
import cv2

# open camera
cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)

# set dimensions
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
    # Display the resulting frame
    cv2.imshow('Frame', frame)
    # Press Q on keyboard to  exit
  if cv2.waitKey(25) & 0xFF == ord('q'):
      break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
