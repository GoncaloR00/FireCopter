#!/usr/bin/env python3

# The function of this node is to recieve information from the get_video node (video) and from the /image/hsv topic
# (HSV parameters) and process that in order to get the centroid of the fire. A possible way to improve this is to add
# functions of machine learning, like openCV cascade or add a thermal camera

import copy
import cv2
import numpy as np
import rospy
from flight_computer.msg import hsv
from sensor_msgs.msg import CompressedImage


class FireDetection:
    def __init__(self):
        # ---------------------------------------------------
        #   Variable declaration
        # ---------------------------------------------------
        self.centroids_list = None
        self.image_np = None
        self.image = None
        self.color_min = np.array([0, 0, 0])
        self.color_max = np.array([255, 255, 255])

        # ---------------------------------------------------
        #   Topics
        # ---------------------------------------------------
        topic_camera = '/image/camera'
        topic_fire_image = '/image/fire'
        topic_fire_hsv = '/image/hsv'
        topic_fire_mask = '/image/mask'

        # ---------------------------------------------------
        #   Subscribers
        # ---------------------------------------------------
        self.firehsv = rospy.Subscriber(topic_fire_hsv, hsv, self.set_hsvCallback)
        self.camera_image = rospy.Subscriber(topic_camera, CompressedImage, self.getCameraCallback)

        # ---------------------------------------------------
        #   Publishers
        # ---------------------------------------------------
        self.publisher = rospy.Publisher(topic_fire_image, CompressedImage, queue_size=5)
        self.maskpub = rospy.Publisher(topic_fire_mask, CompressedImage, queue_size=5)

    def getCameraCallback(self, msg):
        # Uncompress image and convert to an image format
        np_arr = np.frombuffer(msg.data, np.uint8)
        self.image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Variables reset
        self.centroids_list = []

        # Get centroids
        try:
            self.Centroid(self.image_np, self.centroids_list)
        except ():
            rospy.logerr('Error getting centroid')

        # Send image to a topic
        try:
            self.image_out()
        except ():
            rospy.logerr('Error outputing resultant image')

    def set_hsvCallback(self, msg):
        # Get and organize the HSV info from the topic
        self.color_min = np.array([int(msg.hmin), int(msg.smin), int(msg.vmin)])
        self.color_max = np.array([int(msg.hmax), int(msg.smax), int(msg.vmax)])

    def image_out(self):
        # Create a copy of the image, to avoid messing with the original
        imagecopy = copy.deepcopy(self.image_np)

        # Add a mark in the centroid of the fire
        self.image_centroid(imagecopy, self.centroids_list)

        # Compress the image and create a message
        msg = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = "jpeg"
        msg.data = np.array(cv2.imencode('.jpg', imagecopy)[1]).tostring()

        # Publish the message
        self.publisher.publish(msg)


    def image_centroid(self, image, centroid_list):
        # For every centroid finded in the image
        for centroid in centroid_list:
            # Get the coordenates of the centroid (in pixels)
            cX, cY = centroid
            # Draw a circle
            cv2.circle(image, (cX, cY), 5, (0, 0, 0), -1)
            # Add a text below the circle
            cv2.putText(image, 'Alerta', (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    def Centroid(self, image, centroid_data):
        # Convert the image from BGR to HSV to make the color selection esier
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Create a mask
        mask = cv2.inRange(hsv, self.color_min, self.color_max)

        # Join mask and image to make easier to the user to identify the fire when he is ajusting the hsv values
        result = cv2.bitwise_and(image, image, mask=mask)

        # Compress the result and create a message
        sendmask = CompressedImage()
        sendmask.header.stamp = rospy.Time.now()
        sendmask.format = "jpeg"
        sendmask.data = np.array(cv2.imencode('.jpg', result)[1]).tostring()

        # Publish the message
        self.maskpub.publish(sendmask)

        # Get all the centroids off the mask objects
        self.getCentroid(mask, centroid_data)

    def getCentroid(self, mask, centroid_data):
        # Remove some noise of the image
        mask1 = cv2.erode(mask, np.ones((6, 6), np.uint8), iterations=2)
        mask2 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8), iterations=2)
        mask3 = cv2.dilate(mask2, np.ones((6, 6), np.uint8), iterations=2)
        # Get contours
        contours, _ = cv2.findContours(mask3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            # Only big areas
            if cv2.contourArea(c) > 1000:
                # calculate moments for each contour
                M = cv2.moments(c)
                # calculate x,y coordinate of center
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                else:
                    cX, cY = 0, 0
                centroid_data.append((cX, cY))


def main():
    # ---------------------------------------------------
    #   Initialization
    # ---------------------------------------------------
    rospy.init_node('firedetection', anonymous=False)
    fire_detection = FireDetection()
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
