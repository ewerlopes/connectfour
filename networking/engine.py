from autobahn.asyncio.websocket import *
import json
import asyncio
import logging
import threading
import settings


class StoppableThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()


class Engine(StoppableThread):
    def __init__(self, mode):
        StoppableThread.__init__(self)

        self.mode = mode
        self.daemon = True
        self.start()

    def run(self):
        if mode == settings.NETWORK_ENGINE_MODE.HOST:
            self.factory = WebSocketServerFactory()
            self.factory.protocol = ConnectFourServerProtocol

            self.loop = asyncio.get_event_loop()
            self.coro = self.loop.create_server(self.factory, '127.0.0.1', 80)
            self.connection = self.loop.run_until_complete(self.coro)
            self.loop.run_forever()
        elif mode == settings.NETWORK_ENGINE_MODE.JOIN:
            self.factory = WebSocketClientFactory()
            self.factory.protocol = ConnectFourClientProtocol

            self.loop = asyncio.get_event_loop()
            self.coro = self.loop.create_connection(self.factory, '127.0.0.1', 80)
            self.connection = self.loop.run_until_complete(self.coro)
            self.loop.run_forever()

    def stop(self):
        self.connection.close()
        self.loop.close()

        super(Engine, self).stop()


class ConnectFourServerProtocol(WebSocketServerProtocol):
    def onOpen(self):
        logging.info('WebSocket connection open')

    def onConnect(self, request):
        logging.info('Client connecting: {}'.format(request.peer))

    def onClose(self, wasClean, code, reason):
        logging.info('WebSocket connection closed: {}'.format(reason))

    def onMessage(self, payload, isBinary):
        payload = json.loads(payload.decode('utf8'))

        print(payload)

    def sendMessage(self, payload, isBinary):
        payload = json.dumps(payload, ensure_ascii=False).encode('utf8')

        super(WebSocketServerProtocol, self).sendMessage(payload, isBinary)


class ConnectFourClientProtocol(WebSocketClientProtocol):
    def onOpen(self):
        logging.info('WebSocket connection open')

    def onConnect(self, request):
        logging.info('Connected to server: {}'.format(request.peer))

    def onMessage(self, payload, isBinary):
        payload = json.loads(payload.decode('utf8'))

        print(payload)

    def sendMessage(self, payload, isBinary):
        payload = json.dumps(payload, ensure_ascii=False).encode('utf8')

        super(WebSocketClientProtocol, self).sendMessage(payload, isBinary)
