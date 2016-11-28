from interactive import ClientModule
from viewport import Viewport
import requests
import logging
import json
import hashlib

log = logging.getLogger('simple_example')

class Client(ClientModule):
    def __init__(self, password, address="127.0.0.1", port=8080):
        self._address = address
        self._port = port
        self._previous_hash = None
        self._password = password

    def connect(self):
        """Deprecated"""
        pass

    def disconnect(self):
        """Deprecated"""
        pass

    def update(self, viewer):
        log.debug("client.update called")

        map_updates = self._update_map(viewer)

        return map_updates

    def _update_map(self, viewer):
        vp = viewer.get_submodule(Viewport)

        base_url = "http://%s:%s" % (self._address, self._port)

        log.debug("client._update_map requesting map name")
        r = requests.get(base_url + "/map", auth=("user", self._password))
        if r.status_code is not 200:
            log.debug(r.text)
            exit()
        raw_data = r.json()
        map_name = raw_data["map_name"]
        log.debug("client._update_map retrieved map name: %s" % map_name)

        log.debug("client._update_map requesting map hash")
        r = requests.get(base_url + "/map/hash/" + map_name, auth=("user", self._password))
        if r.status_code is not 200:
            log.debug(r.text)
            exit()
        raw_data = r.json()
        new_hash = raw_data["hash"]
        log.debug("client._update_map retrieved map hash: %s, previous hash: %s" % (new_hash, self._previous_hash))

        if new_hash != self._previous_hash:

            r = requests.get(base_url + "/map/data/" + map_name, auth=("user", self._password))
            if r.status_code is not 200:
                log.debug(r.text)
                exit()
            data = r.json()
            data_str = json.dumps(raw_data, sort_keys=True)
            self._previous_hash = new_hash

            if data:
                log.debug("client._update_map read in map name:%s max_y: %s, max_x: %s and %s features from server" %
                        (map_name,
                         data["max_y"],
                         data["max_x"],
                         len(data["features"])))

                viewer.map_name = map_name
                vp.update_features(data["features"])
                vp.update_screen(
                        data["max_y"],
                        data["max_y"])


            return True
        return False
