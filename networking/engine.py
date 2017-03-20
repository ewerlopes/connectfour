from autobahn.asyncio.websocket import *
import json
import asyncio
import logging


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

        super(WebSocketClientProtocol, self).sendMessage(payload, isBinary)


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


def run_server():
    factory = WebSocketServerFactory()
    factory.protocol = ConnectFourServerProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '127.0.0.1', 80)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()


def run_client():
    factory = WebSocketClientFactory()
    factory.protocol = ConnectFourClientProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_connection(factory, '127.0.0.1', 80)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()
