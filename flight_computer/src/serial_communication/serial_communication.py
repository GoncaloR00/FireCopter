#!/usr/bin/env python3
import time

import rospy
import serial
# from std_msgs.msg import String
from flight_computer.msg import TYPR

# ---------------------------------------------------
#   Initialize serial communication
# ---------------------------------------------------
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
ser.reset_input_buffer()
topic_MessageToSend = '/serial/toSend'
# topic_RecivedMessage = '/serial/recieved'

def callback(msg):
    message = ''
    message = str(msg.throttle) + ',' + str(msg.yaw) + ',' + str(msg.pitch) + ',' + \
              str(msg.roll) + ',' + "\n"
    print(message)
    ser.write(message.encode('utf-8'))
    # ser.read(10)
    # ser.timeout = 0.02

def serial_communication():
    # while True:
        # line = ser.readline().decode('latin-1').rstrip()
        # print(line)
        # ---------------------------------------------------
        #   Topics to subscribe and subscription
        # ---------------------------------------------------
    rospy.Subscriber(topic_MessageToSend, TYPR, callback)
    # time.sleep(0.1)
        # ---------------------------------------------------
        #   Topics to publish and publication
        # ---------------------------------------------------
        # pub = rospy.Publisher(topic_RecivedMessage, String, queue_size=1)
        # ser.read(10)
        # ser.timeout = 0.02
        # test = str(ser.readline().decode('latin-1').rstrip())
        # pub.publish(test)
        # rate = rospy.Rate(10)
        # print('ok1')
    # rospy.spin()


def main():
    # ---------------------------------------------------
    #   Initialization
    # ---------------------------------------------------
    rospy.init_node('serial_comunicatiom', anonymous=False)
    serial_communication()
    rospy.spin()
    # rospy.spin()


if __name__ == '__main__':
    main()
    try:
        main()
    except rospy.ROSInterruptException:
        print(rospy.ROSInterruptException)
