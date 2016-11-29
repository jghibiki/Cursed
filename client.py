from interactive import ClientModule
from viewport import Viewport
import requests
import logging
import json
import hashlib

log = logging.getLogger('simple_example')

class Client(ClientModule):
    def __init__(self, password, map_name=None, host="127.0.0.1", port=8080):
        self._host = host
        self._port = port
        self._previous_hash = None
        self._previous_feature_hashes = []
        self._password = password
        self._base_url = "http://%s:%s" % (self._host, self._port)
        self._map_name = map_name

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

        log.debug("client._update_map requesting map name")
        raw_data = self.make_request("/map")
        self._map_name = raw_data["map_name"]
        log.debug("client._update_map retrieved map name: %s" % self._map_name)

        log.debug("client._update_map requesting map hash")
        raw_data = self.make_request("/map/hash/%s" % self._map_name)
        new_hash = raw_data["hash"]
        log.debug("client._update_map retrieved map hash: %s, previous hash: %s" % (new_hash, self._previous_hash))

        if new_hash != self._previous_hash:

            data = self.make_request("/map/data/%s" % self._map_name)
            self._previous_hash = new_hash

            if data:
                log.debug("client._update_map read in map name:%s max_y: %s, max_x: %s and %s features from server" %
                        (self._map_name,
                         data["max_y"],
                         data["max_x"],
                         len(data["features"])))

                viewer.map_name = self._map_name
                vp.update_features(data["features"])
                vp.update_screen(
                        data["max_y"],
                        data["max_y"])

                return True
        return False

    def make_request(self, url, payload=None):
        if not payload:
            log.debug("make_request GET %s" % url)
            r = requests.get(self._base_url + url, auth=("user", self._password))
        else:
            log.debug("make_request POST %s %s" % (url, payload))
            r = requests.post(self._base_url + url,
                              auth=("user", self._password),
                              headers={'content-type': 'application/json'},
                              data=json.dumps(payload))

        if r.status_code is not 200: # TODO: fix naiive checl
            log.warn("make_request http error: %s %s %s" % (url, r.status_code, r.text))

        # try to get json
        try:
            raw_data = r.json()
            return raw_data
        except:
            return None

