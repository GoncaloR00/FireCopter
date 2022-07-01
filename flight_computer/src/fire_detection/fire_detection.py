#!/usr/bin/env python3
import copy
import cv2
import numpy as np
import rospy
from flight_computer.msg import hsv
from sensor_msgs.msg import CompressedImage


class FireDetection:
    def __init__(self):
        self.centroids_list = None
        self.image_np = None
        self.color_min = np.array([0, 181, 144])
        self.color_max = np.array([101, 255, 255])
        self.image = None
        # ---------------------------------------------------
        #   Topics
        # ---------------------------------------------------
        topic_camera = '/image/camera'
        topic_fire_image = '/image/fire'
        topic_fire_hsv = '/image/hsv'
        topic_fire_mask = '/image/mask'

        # ---------------------------------------------------
        #   Subscription
        # ---------------------------------------------------
        self.firehsv = rospy.Subscriber(topic_fire_hsv, hsv, self.set_hsvCallback)
        self.camera_image = rospy.Subscriber(topic_camera, CompressedImage, self.getCameraCallback)
        self.publisher = rospy.Publisher(topic_fire_image, CompressedImage, queue_size=5)
        self.maskpub = rospy.Publisher(topic_fire_mask, CompressedImage, queue_size=5)

    def getCameraCallback(self, msg):
        np_arr = np.frombuffer(msg.data, np.uint8)
        self.image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        # Variables reset
        self.centroids_list = []
        # Get centroids
        try:
            self.Centroid(self.image_np, self.centroids_list)
        except ():
            rospy.logerr('Error getting centroid')
        try:
            self.image_out()
        except ():
            rospy.logerr('Error outputing resultant image')

    def set_hsvCallback(self, msg):
        self.color_min = np.array([int(msg.hmin), int(msg.smin), int(msg.vmin)])
        self.color_max = np.array([int(msg.hmax), int(msg.smax), int(msg.vmax)])

    def image_out(self):
        imagecopy = copy.deepcopy(self.image_np)
        self.image_centroid(imagecopy, self.centroids_list)
        msg = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = "jpeg"
        msg.data = np.array(cv2.imencode('.jpg', imagecopy)[1]).tostring()
        self.publisher.publish(msg)


    def image_centroid(self, image, centroid_list):
        for centroid in centroid_list:
            cX, cY = centroid
            cv2.circle(image, (cX, cY), 5, (0, 0, 0), -1)
            cv2.putText(image, 'Alerta', (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    def Centroid(self, image, centroid_data):

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.color_min, self.color_max)
        result = cv2.bitwise_and(image, image, mask=mask)
        sendmask = CompressedImage()
        sendmask.header.stamp = rospy.Time.now()
        sendmask.format = "jpeg"
        sendmask.data = np.array(cv2.imencode('.jpg', result)[1]).tostring()
        self.maskpub.publish(sendmask)
        self.getCentroid(mask, centroid_data)

    def getCentroid(self, mask, centroid_data):
        # Remove noise from mask
        # maskcopy = mask.copy()
        # cnts_aux1, _ = cv2.findContours(maskcopy, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # for c in cnts_aux1:
        #     area = cv2.contourArea(c)
        #     if area > 25:
        #         cv2.drawContours(maskcopy, c, -1, (255, 255, 255), 25)
        mask1 = cv2.erode(mask, np.ones((6, 6), np.uint8), iterations=2)
        mask2 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8), iterations=2)
        mask3 = cv2.dilate(mask2, np.ones((6, 6), np.uint8), iterations=2)
        # Get new contours
        contours, _ = cv2.findContours(mask3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
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
