from interactive import ClientModule
from socket_server import JsonClient
from viewport import Viewport

class Client(ClientModule):
    def __init__(self, address="127.0.0.1", port=5489):
        self._address = address
        self._port = port
        self._client = None

    def connect(self):
        self._client = JsonClient(
                address=self._address,
                port=self._port)
        self._client.connect()

    def disconnect(self):
        self._client.close()
        self._client = None

    def update(self, viewer):
        vp = viewer.get_submodule(Viewport)
        self._client.send({"command": "get"})
        data = self._client.read()

        viewer.map_name = data["name"]
        vp.update_features(data["data"])
        vp.update_screen(
                data["max_y"],
                data["max_y"])


