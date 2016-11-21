from interactive import ServerModule
from socket_server import Server as ThreadedJsonServer
from viewport import Viewport
import queue

class Server(ServerModule):

    def __init__(self):
        self._queue = queue.Queue()
        self._server = ThreadedJsonServer(self._queue)
        self._server.start()

    def update(self, viewer):
        vp = viewer.get_submodule(Viewport)
        feature_data = vp.serialize_features()
        try:
            self._queue.put_nowait({
                "name": viewer.map_name,
                "max_y": vp.h,
                "max_x": vp.w,
                "data": feature_data
            })
        except queue.Full:
            pass

    def stop(self):
        self._server.stop()
