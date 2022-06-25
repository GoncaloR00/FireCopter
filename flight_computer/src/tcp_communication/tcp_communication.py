#!/usr/bin/env python3
import rospy
import socket
import threading
import struct
from flight_computer.msg import TYPR

topic_MessageToSend = '/serial/toSend'
topic_RecivedMessage = '/serial/recieved'
pub = rospy.Publisher(topic_MessageToSend, TYPR, queue_size=1)

# Connection Data
host = socket.gethostname()
port = 2022

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []


# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)


# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            # aux = message.decode('ascii').split(',')
            aux = struct.unpack('!iiii', message)
            msg = TYPR()
            msg.throttle = aux[0]
            msg.yaw = aux[1]
            msg.pitch = aux[2]
            msg.roll = aux[3]
            print(aux)
            pub.publish(msg)
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            # broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break


# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def main():
    # ---------------------------------------------------
    #   Initialization
    # ---------------------------------------------------
    rospy.init_node('TCP_Receiver', anonymous=False)
    receive()
    # rospy.spin()


if __name__ == '__main__':
    main()
    try:
        main()
    except rospy.ROSInterruptException:
        print(rospy.ROSInterruptException)