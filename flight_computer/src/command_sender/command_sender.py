#!/usr/bin/env python3

# Not done yet! The function of this node is to recieve information from the xyz_control node and from the
# tcp_communication node and send information to the serial_communication node. From the tcp_communication (Joystick
# data) the recieved message will include a variable "mode".

# If mode == true, then we are in automatic mode, witch means that the Throttle, pitch, roll and yaw values to listen
# are from the xyz_control

# If mode == false, then we are in manual mode, witch means that the Throttle, pitch, roll and yaw values to listen
# are from the tcp_communication
