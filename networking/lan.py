import time
import socket
import threading
import settings


class StoppableThread(threading.Thread):
    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()


class Announce(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.daemon = True
        self.start()

    def stop(self):
        self.s.close()
        self.stop()

    def run(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.s.bind(('', 0))
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        my_ip = socket.gethostbyname(socket.getfqdn())
        data = str.encode('-'.join([settings.LAN_IDENTIFIER, my_ip]))

        while True:
            if self.stopped():
                break

            self.s.sendto(data, ('<broadcast>', settings.LAN_PORT))
            time.sleep(5)


class Discover(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.daemon = True
        self.start()

    def stop(self):
        self.s.close()
        self.stop()

    def run(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.s.bind(('', settings.LAN_PORT))

        while True:
            if self.stopped():
                break

            data = self.s.recv(512)

            if data:
                data = data.decode().split('-')

                if len(data) == 2 and data[0] == settings.LAN_IDENTIFIER:
                    print('{} seems to host a Connect Four LAN game'.format(data[1])) # TODO
