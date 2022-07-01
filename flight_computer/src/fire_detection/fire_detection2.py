#!/usr/bin/env python3
import copy
import cv2
import numpy as np
import rospy
from flight_computer.msg import hsv
from sensor_msgs.msg import CompressedImage

# ---------------------------------------------------
#   Topics
# ---------------------------------------------------
topic_camera = '/image/camera'
topic_fire_image = '/image/fire'
topic_fire_hsv = '/image/hsv'
topic_fire_mask = '/image/mask'


def getCameraCallback(msg):
    # Variables reset
    centroids_list = []
    np_arr = np.frombuffer(msg.data, np.uint8)
    image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Get centroids
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])

    # Convert to HSV format and color threshold
    hsv = cv2.cvtColor(image_np, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(image_np, image_np, mask=mask)
    sendmask = CompressedImage()
    sendmask.header.stamp = rospy.Time.now()
    sendmask.format = "jpeg"
    sendmask.data = np.array(cv2.imencode('.jpg', result)[1]).tostring()
    maskpub.publish(sendmask)


rospy.init_node('firedetection', anonymous=False)
# firehsv = rospy.Subscriber(topic_fire_hsv, hsv, set_hsvCallback)
camera_image = rospy.Subscriber(topic_camera, CompressedImage, getCameraCallback)
publisher = rospy.Publisher(topic_fire_image, CompressedImage, queue_size=5)
maskpub = rospy.Publisher(topic_fire_mask, CompressedImage, queue_size=5)

# Initialize HSV min/max values
hMin = sMin = vMin = hMax = sMax = vMax = 0
hMax = 150
sMax = 255
vMax = 255



def main():
    # ---------------------------------------------------
    #   Initialization
    # ---------------------------------------------------

    # fire_detection = FireDetection()
    # ---------------------------------------------------
    #   Execution
    # ---------------------------------------------------
    rate = rospy.Rate(10)
    rate.sleep()
    rospy.spin()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
