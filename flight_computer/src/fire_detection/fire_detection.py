#!/usr/bin/env python3
import copy
import cv2
import numpy as np
import rospy
from flight_computer.msg import hsv
from sensor_msgs import CompressedImage

class FireDetection():
    def __init__(self):
        self.image_np = None
        self.color_min = np.array([0, 0, 0])
        self.color_max = np.array([0, 0, 0])
        self.image = None
        # ---------------------------------------------------
        #   Topics
        # ---------------------------------------------------
        topic_camera = '/image/camera'
        topic_fire_image = '/image/fire'
        topic_fire_hsv = '/image/hsv'

        # ---------------------------------------------------
        #   Subscription
        # ---------------------------------------------------
        self.firehsv = rospy.Subscriber(topic_fire_hsv, hsv, self.set_hsvCallback)
        self.camera_image = rospy.Subscriber(topic_camera, CompressedImage, self.getCameraCallback)

        self.publisher = rospy.Publisher(topic_fire_image, CompressedImage)

    def getCameraCallback(self, msg):
        np_arr = np.fromstring(msg.data, np.uint8)
        self.image_np = cv2.imdecode(np_arr, cv2.CV_LOAD_IMAGE_COLOR)
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
        self.color_min = np.array([msg.hmin, msg.smin, msg.vmin])
        self.color_max = np.array([msg.hmax, msg.smax, msg.vmax])

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
        mask_team = cv2.inRange(image, self.color_min, self.color_max)
        self.getCentroid(mask_team, centroid_data)

    def getCentroid(self, mask, centroid_data):
        # Remove noise from mask
        maskcopy = mask.copy()
        cnts_aux1, _ = cv2.findContours(maskcopy, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts_aux1:
            area = cv2.contourArea(c)
            if area > 25:
                cv2.drawContours(maskcopy, c, -1, (255, 255, 255), 25)
        mask2 = cv2.morphologyEx(maskcopy, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8), iterations=2)
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
        rospy.init_node('p_g3_driver', anonymous=False)
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