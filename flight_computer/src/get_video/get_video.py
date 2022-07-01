#!/usr/bin/env python3
import rospy
import cv2
from sensor_msgs.msg import CompressedImage
import numpy as np

rospy.init_node('get_video', anonymous=False)
topic = '/image/camera'
pub = rospy.Publisher(topic, CompressedImage, queue_size=5)
rate = rospy.Rate(10)
# open camera
cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
# set dimensions
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


def talker():
    while not rospy.is_shutdown():
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if ret:
        #     # Display the resulting frame
        #     cv2.imshow('Frame', frame)
        #     # Press Q on keyboard to  exit
        # if cv2.waitKey(25) & 0xFF == ord('q'):
        #     break
        msg = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = "jpeg"
        msg.data = np.array(cv2.imencode('.jpg', frame)[1]).tostring()
        pub.publish(msg)
        rate.sleep()

# When everything done, release the video capture object


# Closes all the frames


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
    cap.release()
    cv2.destroyAllWindows()
