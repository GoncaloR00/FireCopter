#!/usr/bin/env python3

# This node is not working the way it is supposed to be. There are some problems and the message sometimes is not
# sendded our recieved in the right way

# The function of this node is to send commands of Throttle, pitch, roll and yaw form the command_sender node to the
# flight controller and to recieve the angle data from the flight controller and send to the interface

import time
import rospy
import serial
from flight_computer.msg import TYPR
from flight_computer.msg import SensorData


class Serial_communication:
    def __init__(self):
        # ---------------------------------------------------
        #   Initialize serial communication
        # ---------------------------------------------------
        self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        self.ser.reset_input_buffer()
        # ---------------------------------------------------
        #   Topics
        # ---------------------------------------------------
        topic_MessageToSend = '/serial/toSend'
        topic_RecivedMessage = '/serial/recieved'
        # ---------------------------------------------------
        #   Topics Subscription
        # ---------------------------------------------------
        self.toSend = rospy.Subscriber(topic_MessageToSend, TYPR, self.send)
        # ---------------------------------------------------
        #   Publish functions
        # ---------------------------------------------------
        self.timer = rospy.Timer(rospy.Duration(0.1), self.recieve)
        self.recieved = rospy.Publisher(topic_RecivedMessage, SensorData, queue_size=1)

    def send(self, msg):
        message = ''
        # Create a message to send (in a specific format)
        message = str(msg.throttle) + ',' + str(msg.yaw) + ',' + str(msg.pitch) + ',' + \
                  str(msg.roll) + ',' + str(msg.arm) + ',' + str(msg.sos) + ',' + "\n"
        print(message)
        # Send the message
        self.ser.write(message.encode('utf-8'))
        time.sleep(0.1)

    def recieve(self, event):
        # Recieve the message and convert to string
        line = str(self.ser.readline().decode('latin-1').rstrip())
        # Separate the x angle form the y angle
        recieved = line.split(',')
        print(recieved)
        time.sleep(0.1)
        # In case of no message set angles to zero (shoud be other value to indicate error)
        x_anglev = 0
        y_anglev = 0
        # If there is a message, convert to integer
        try:
            x_anglev = int(float(recieved[0]))
            y_anglev = int(float(recieved[0]))
        except:
            pass
        # Create a message
        msg = SensorData()
        msg.x_angle = x_anglev
        msg.y_angle = y_anglev
        # Send the message
        self.recieved.publish(msg)


def main():
    # ---------------------------------------------------
    #   Initialization
    # ---------------------------------------------------
    rospy.init_node('serial_communication', anonymous=False)
    serial = Serial_communication()
    # ---------------------------------------------------
    #   Execution
    # ---------------------------------------------------
    rate = rospy.Rate(100)
    rate.sleep()
    rospy.spin()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
