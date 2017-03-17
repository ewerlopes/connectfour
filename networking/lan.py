import time
import socket
import threading
import constants


class Announce(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.daemon = True
        self.start()

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        my_ip = socket.gethostbyname(socket.gethostname())
        data = str.encode('-'.join([constants.LAN_IDENTIFIER, my_ip]))

        while True:
            s.sendto(data, ('<broadcast>', constants.LAN_PORT))
            time.sleep(5)


class Discover(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.daemon = True
        self.start()

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        s.bind(('', constants.LAN_PORT))

        while True:
            data, addr = s.recvfrom(1024)

            data = data.decode()

            if data.startswith(constants.LAN_IDENTIFIER):
                print('{} answered'.format(data[len(constants.LAN_IDENTIFIER) + 1:]))
