#!/usr/bin/env python3
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
        #   Subscription
        # ---------------------------------------------------
        self.toSend = rospy.Subscriber(topic_MessageToSend, TYPR, self.send)
        # ---------------------------------------------------
        #   Pub
        # ---------------------------------------------------
        self.timer = rospy.Timer(rospy.Duration(0.1), self.recieve)
        self.recieved = rospy.Publisher(topic_RecivedMessage, SensorData, queue_size=1)

    def send(self, msg):
        message = ''
        message = str(msg.throttle) + ',' + str(msg.yaw) + ',' + str(msg.pitch) + ',' + \
                  str(msg.roll) + ',' + str(msg.arm) + ',' + str(msg.sos) + ',' + "\n"
        print(message)
        self.ser.write(message.encode('utf-8'))
        time.sleep(0.1)
        # ser.read(10)
        # ser.timeout = 0.02

    def recieve(self, event):
        line = str(self.ser.readline().decode('latin-1').rstrip())
        recieved = line.split(',')
        print(recieved)
        time.sleep(0.1)
        x_anglev = 0
        y_anglev = 0
        try:
            x_anglev = int(float(recieved[0]))
            y_anglev = int(float(recieved[0]))
        except:
            pass
        msg = SensorData()
        msg.x_angle = x_anglev
        msg.y_angle = y_anglev
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
