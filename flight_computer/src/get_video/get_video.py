#!/usr/bin/env python3
import rospy
import cv2
from sensor_msgs.msg import CompressedImage
import numpy as np

# Initialize the node
rospy.init_node('get_video', anonymous=False)
# Topic to publish
topic = '/image/camera'
# Publishing function
pub = rospy.Publisher(topic, CompressedImage, queue_size=5)
rate = rospy.Rate(10)
# Open camera
cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
# Set dimensions
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


def talker():
    while not rospy.is_shutdown():
        # Capture the frame
        ret, frame = cap.read()
        # Create a message with the image in a compressed format
        msg = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = "jpeg"
        msg.data = np.array(cv2.imencode('.jpg', frame)[1]).tostring()
        # Publish the message
        pub.publish(msg)
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
    # Termination
    cap.release()
