import socket

class OssConnectionException(socket.error):
    def __init__(self, error):
        self.error = error