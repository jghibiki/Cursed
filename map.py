from interactive import LiveModule, InteractiveModule, TextDisplayModule
from client import Client
from viewport import Viewport
from unit import Unit
from text_box import TextBox
import logging
import re

log = logging.getLogger('simple_example')

class Map(LiveModule, InteractiveModule, TextDisplayModule):
    def __init__(self):
        self._previous_map_hash = "bad_hash"
        self._previous_fow_hash = "bad_hash"
        self._previous_unit_hash = "bad_hash"
        self._previous_note_hash = "bad_hash"
        self._showing = False
        self._maps = []

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

        unit_hash = hashes["unit"]
        if unit_hash != self._previous_unit_hash:
            self._previous_unit_hash = unit_hash
            data = client.make_request('/unit')

            if data:
                units = [ Unit(unit) for unit in data["units"] ]
                vp.update_units(units)
                updates = True


        return updates

    def force_update(self, viewer):
        vp = viewer.get_submodule(Viewport)
        client = viewer.get_submodule(Client)

        # update features
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


        # update fow
        data = client.make_request("/fow")

        if data:
            vp.update_fow(data["fow"])


        # update units
        data = client.make_request('/unit')

        if data:
            units = [ Unit(unit) for unit in data["units"] ]
            vp.update_units(units)


    def _handle(self, viewer, ch):
        pass

    def _handle_help(self, viewer, buf):
        pass

    def _handle_combo(self, viewer, buf):
        split = buf.split(" ")
        if len(split) == 1 and (split[0] == "map" or split[0] == "m"):
            self._show(viewer)

        elif len(split) == 4 and (split[0] == "map" or split[0] == "m") and (split[1] == "move" or split[1] == "m"):
            from users import Users
            users = viewer.get_submodule(Users)

            regex = split[2]
            map_to_switch = split [3]

            valid_map = False
            for map_name in self._maps:
                if map_name == map_to_switch:
                    valid_map = True
                    break

            if valid_map:

                usernames = [ user["username"] for user in users.users ]

                if len(regex) == 1 and regex == "*":
                    regex = ".*"
                regex = re.compile(regex)

                filtered_usernames = filter(regex.match, usernames)

                client = viewer.get_submodule(Client)

                for username in usernames:

                    data = client.make_request("/map", payload={
                        "username": username,
                        "map_name": map_to_switch
                    })



    def _show(self, viewer):
        self._showing = True
        viewer.apply_to_submodules(TextDisplayModule, lambda x: x._hide(viewer))
        self.show_maps(viewer)

    def _hide(self, viewer):
        self._showing = False

    def get_maps(self, viewer):

        client = viewer.get_submodule(Client)

        data = client.make_request("/map")
        self._maps = sorted(data["maps"])

    def show_maps(self, viewer):
        tb = viewer.get_submodule(TextBox)

        self.get_maps(viewer)

        from users import Users
        users = viewer.get_submodule(Users)

        lines = [ [{
            "text": "Maps:",
            "color": "Gold"
        }] ]
        for map_name in self._maps:
            lines.append([{
                "text": "{0}".format(map_name),
                "color": "Gold"
            }])

            for user in users.users:
                if user["current_map"] == map_name:
                    lines.append([{
                        "text": "- {0}".format(user["username"]),
                        "color": None
                    }])

        tb.set(lines)
