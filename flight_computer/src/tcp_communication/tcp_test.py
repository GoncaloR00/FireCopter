#!/usr/bin/env python3

import socket
import threading
import pickle
# import rospy
# from flight_computer.msg import TYPR

# topic_MessageToSend = '/serial/toSend'
# topic_RecivedMessage = '/serial/recieved'
# pub = rospy.Publisher(topic_MessageToSend, TYPR, queue_size=1)

# Connection Data
host = socket.gethostname()
port = 2022

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(1)


# Handling Messages From Clients and sending to the respective topics
def handle(client):
    while True:
        try:
            message = client.recv(200)
            if not message:
                print('HELP')
                # TODO meter led de alerta
                break
            aux1 = pickle.loads(message)
            # print(type(aux1))
            # throttle = aux1[0]
            # print(throttle)
            (throttle, yaw, pitch, roll, start, stop, sos, mode) = aux1
            print(aux1)
            # msg = TYPR()
            # msg.throttle = throttle
            # msg.yaw = yaw
            # msg.pitch = pitch
            # msg.roll = roll
            # pub.publish(msg)
            # old_message = aux
            # time.sleep(0.1)
        except Exception as e:
            print('Error: ', e)


# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


def main():
    # ---------------------------------------------------
    #   Initialization
    # ---------------------------------------------------
    # rospy.init_node('TCP_Receiver', anonymous=False)
    receive()
    # rospy.spin()


if __name__ == '__main__':
    main()
    # try:
    #     main()
    # except rospy.ROSInterruptException:
    #     print(rospy.ROSInterruptException)
