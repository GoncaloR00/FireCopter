
from abc import ABC, abstractmethod


class ClassAbstractServer(ABC):

    def __init__(self):
        self.is_started = False

    def start(self, port):
        if self.is_started is True:
            print('Cannot start. Already started!')
            return False

        if self._start(port):
            self.is_started = True
            return True
        else:
            return False

    @abstractmethod
    def _start(self, port):
        return

    def stop(self):
        if not self.is_started:
            print('Cannot stop. Already stopped!')
            return False

        if self._stop():
            self.is_started = False
            return True
        else:
            return False

    @abstractmethod
    def _stop(self):
        return

    # def handle(self, client):
    #     if self.is_started is False:
    #         print('Cannot handle. Server offline!')
    #         return False
    #     return self._receive(client)
    #
    # @abstractmethod
    # def _handle(self, client):
    #     return

    def receive(self, msg):
        if self.is_started is False:
            print('Cannot receive. Server offline!')
            return False

        return self._receive(msg)

    @abstractmethod
    def _receive(self, msg):
        return

    def send(self, msg):
        if self.is_started is False:
            print('Cannot setData. Hardware disconnected!')
            return False

        return self._send(msg)

    @abstractmethod
    def _send(self, msg):
        return