import socket
import threading
from ClassAbstractServer import ClassAbstractServer


class ClassTCP(ClassAbstractServer):

    def __init__(self):
        super().__init__()

    def _start(self, port):
        host = 'localhost'
        # Starting Server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        server.listen()
        # Lists For Clients and Their Nicknames
        self.clients = []
        self.nicknames = []
        return True

    def _stop(self):
        return False

    def _receive(self, msg):
        return True

    def _send(self, msg):
        
        return True