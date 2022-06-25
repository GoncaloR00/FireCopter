#!/usr/bin/env python3
import rospy
import serial
from std_msgs.msg import String
from flight_computer.msg import TYPR, SensorData

# ---------------------------------------------------
#   Initialize serial communication
# ---------------------------------------------------
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
ser.reset_input_buffer()
topic_MessageToSend = '/serial/toSend'
topic_RecivedMessage = '/serial/recieved'

def callback(msg):
    message = str(int(msg.throttle)) + ',' + str(int(msg.yaw)) + ',' + str(int(msg.pitch)) + ',' + \
              str(int(msg.roll)) + ',' + "\n"
    ser.write(message.encode('utf-8'))

def serial_communication():
    while True:
        # ---------------------------------------------------
        #   Topics to subscribe and subscription
        # ---------------------------------------------------
        rospy.Subscriber(topic_MessageToSend, TYPR, callback)
        # ---------------------------------------------------
        #   Topics to publish and publication
        # ---------------------------------------------------
        pub = rospy.Publisher(topic_RecivedMessage, String, queue_size=1)
        ser.read(10)
        ser.timeout = 0.02
        test = str(ser.readline().decode('latin-1').rstrip())
        pub.publish(test)
        rate = rospy.Rate(10)
        print('ok1')
    # rospy.spin()


def main():
    # ---------------------------------------------------
    #   Initialization
    # ---------------------------------------------------
    rospy.init_node('serial_comunicatiom', anonymous=False)
    serial_communication()
    # rospy.spin()


if __name__ == '__main__':
    main()
    try:
        main()
    except rospy.ROSInterruptException:
        print(rospy.ROSInterruptException)
