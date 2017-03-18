import time
import socket
import threading
import settings
import logging
import platform
import json


class StoppableThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()


class LanGame(StoppableThread):
    def __init__(self):
        StoppableThread.__init__(self)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.daemon = True
        self.start()

    def stop(self):
        self.s.close()
        super(LanGame, self).stop()


class Announcer(LanGame):
    def __init__(self):
        logging.info('Running Announcer thread')

        LanGame.__init__(self)

    def run(self):
        self.s.bind(('', 0))
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        data = [
            settings.LAN_IDENTIFIER,
            socket.gethostbyname(socket.getfqdn()),
            platform.node()
        ]

        data = str.encode(json.dumps(data))

        while True:
            if self.stopped():
                break

            self.s.sendto(data, ('<broadcast>', settings.LAN_PORT))
            time.sleep(5)


class Discoverer(LanGame):
    def __init__(self):
        logging.info('Running Discoverer thread')

        LanGame.__init__(self)

    def run(self):
        self.s.bind(('', settings.LAN_PORT))

        while True:
            if self.stopped():
                break

            data = self.s.recv(512).decode()

            if data:
                data = json.loads(data)

                print(data)

                lan_identifier, host_ip, host_name = data

                if lan_identifier == settings.LAN_IDENTIFIER:
                    print('{} ({}) seems to host a Connect Four LAN game'.format(host_ip, host_name)) # TODO
