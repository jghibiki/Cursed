from autobahn.asyncio.websocket import WebSocketClientProtocol
from autobahn.asyncio.websocket import WebSocketClientFactory

import logging

log = logging.getLogger('simple_example')

class BroadcastClientProtocol(WebSocketClientProtocol):

    def __init__(self, *args, **kwargs):
        super(WebSocketClientProtocol, self).__init__(*args, **kwargs)

        self.clients = []

    def onOpen(self):
        self.factory.register(self)

    def onConnect(self, client):
        log.info("Client connecting: {}".format(client.peer))
        self.clients.append(client)


    def onMessage(self, payload, isBinary):

        # deserialize json
        obj = json.loads(payload.decode("utf8"))

        if("CURSED_MAGIC_DEBUG" in os.environ
            and os.environ["CURSED_MAGIC_DEBUG"]):
            log.info(obj["type"], obj["key"] if "key" in obj else None)


        success = False #don't allow a broadcast on a bad handle

        if(obj["type"] == "ping"):
            self.send({"type": "pong"})
            success = True

        elif(obj["type"] == "register"):
            self.register(obj["id"])
            success = True

#        elif(obj["type"] == "command" and obj["key"] != "bulk"):
#            if(obj["key"] in magic.subscriptions.common_handlers):
#                if(obj["password"] == magic.gm_password
#                    or obj["password"] == magic.password):
#                    for handler in magic.subscriptions.common_handlers[obj["key"]]:
#                        success = handler(self, obj) or success
#
#            if(obj["key"] in magic.subscriptions.gm_handlers):
#                if obj["password"] == magic.gm_password:
#                    for handler in magic.subscriptions.gm_handlers[obj["key"]]:
#                        success = handler(self, obj) or success
#
        elif(obj["type"] == "command" and obj["key"] == "bulk"):
            if "frames" in obj:
                pass
#                success = True
#                for frame in obj["frames"]:
#                    if(frame["key"] in magic.subscriptions.common_handlers):
#                        if(obj["password"] == magic.gm_password
#                            or obj["password"] == magic.password):
#                            for handler in magic.subscriptions.common_handlers[frame["key"]]:
#                                handler(self, frame)
#
#                    if(frame["key"] in magic.subscriptions.gm_handlers):
#                        if obj["password"] == magic.gm_password:
#                            for handler in magic.subscriptions.gm_handlers[frame["key"]]:
#                                handler(self, frame)
            else:
                client.sendTarget(
                        req["id"],
                        type="error",
                        key="modify.map.fow",
                        payload={"msg": "Request details missing \"x\""})

        # if broadcast == true broadcast to all
        if("broadcast" in obj
            and obj["broadcast"]
            and success):
            self.broadcast(obj)

    def connectionLost(self, reason):
        WebSocketClientProtocol.connectionLost(self, reason)
        self.factory.unregister(self)

    def register(self, id):
        self.clients.append(id)

    def broadcast(self, payload):
        self.send(payload, type="broadcast")

    def send(self, payload, type=None, key=None, isResponse=False):
        if type is not None:
            payload["type"] = type

        if key is not None:
            payload["key"] = key

        payload["is_response"] = isResponse

        if("CURSED_MAGIC_DEBUG" in os.environ
            and os.environ["CURSED_MAGIC_DEBUG"]):
            log.info(payload["type"], payload["key"] if "key" in payload else None)

        payload = json.dumps(payload, ensure_ascii=False).encode("utf8")

        if type == "broadcast":
            if("CURSED_MAGIC_DEBUG" in os.environ
                and os.environ["CURSED_MAGIC_DEBUG"]):
                log.info("broadcasting")
            self.factory.broadcast(payload)
        else:
            self.sendMessage(payload)


class MagicBroadcastClientFactory(WebSocketClientFactory):

    protocol = BroadcastClientProtocol

    def __init__(self):
        WebSocketClientFactory.__init__(self)
        self.client = None


    def _registerClient(self, client):
        self.client = client

    def _unregisterClient(self, client):
        self.client = None

    def send(self, payload):
        if self.client:
            self.client.sendMessage(payload)
        else:
            log.warn("Attempted to send when no client connection has been established.")

    def broadcast(self, payload): #TODO determine how broadcast will be different then send from a client perspective - should just be a param in the payload
        if self.client:
            self.client.sendMessage(payload)
        else:
            log.warn("Attempted to send when no client connection has been established.")


def start_client(host, port, viewer):

    try:
       import asyncio
    except ImportError:
       ## Trollius >= 0.3 was renamed
       import trollius as asyncio


    factory = MagicBroadcastClientFactory()

    loop = asyncio.get_event_loop()

    viewer.setLoop(loop)
    viewer.setClient(factory)
    loop.call_soon(viewer.tick)

    coro = loop.create_connection(factory, host, port)
    server = loop.run_until_complete(coro)

    try:
       loop.run_forever()
    except KeyboardInterrupt:
       pass
    finally:
       server.close()
       loop.close()
