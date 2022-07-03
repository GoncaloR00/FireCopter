#!/usr/bin/env python3

# This is a temporary node! This only exist because we had problems with sending a recieving messages at the same
# time. This turn out to be a temporary solution to ONLY send info to the flight controller

import rospy
import serial
from flight_computer.msg import TYPR

# ---------------------------------------------------
#   Initialize serial communication
# ---------------------------------------------------
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
ser.reset_input_buffer()

# ---------------------------------------------------
#   Topics to subscribe
# ---------------------------------------------------
topic_MessageToSend = '/serial/toSend'

def callback(msg):
    message = ''
    # Create a message to send (in a specific format)
    message = str(msg.throttle) + ',' + str(msg.yaw) + ',' + str(msg.pitch) + ',' + \
              str(msg.roll) + ',' + str(msg.arm) + ',' + str(msg.sos) + ',' + "\n"
    print(message)
    # Send the message
    ser.write(message.encode('utf-8'))

def serial_communication():
    # ---------------------------------------------------
    #   Topics subscription and function calling
    # ---------------------------------------------------
    rospy.Subscriber(topic_MessageToSend, TYPR, callback)



def main():
    # ---------------------------------------------------
    #   Initialization
    # ---------------------------------------------------
    rospy.init_node('serial_comunicatiom', anonymous=False)
    serial_communication()
    rospy.spin()


if __name__ == '__main__':
    main()
    try:
        main()
    except rospy.ROSInterruptException:
        print(rospy.ROSInterruptException)
