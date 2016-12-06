from interactive import LiveModule
from client import Client
from viewport import Viewport
import logging

log = logging.getLogger('simple_example')

class Map(LiveModule):
    def __init__(self):
        self._previous_map_hash = None
        self._previous_fow_hash = None

    def _update(self, viewer, hashes):
        vp = viewer.get_submodule(Viewport)
        client = viewer.get_submodule(Client)

        new_hash = hashes["map"]
        updates = False
        if new_hash != self._previous_map_hash:
            self._previous_map_hash = new_hash

            data = client.make_request("/map/data/")

            if data:
                log.debug("client._update_map read in max_y: %s, max_x: %s and %s features from server" %
                        (data["max_y"],
                         data["max_x"],
                         len(data["features"])))

                vp.update_features(data["features"])
                vp.update_screen(
                        data["max_y"],
                        data["max_y"])

                updates = True

        fow_hash = hashes["fow"]
        if fow_hash != self._previous_fow_hash:
            self._previous_fow_hash = fow_hash
            data = client.make_request("/fow")

            if data:
                vp.update_fow(data["fow"])
                updates = True


        return updates
