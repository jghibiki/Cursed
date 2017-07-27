from interactive import LiveModule, InteractiveModule, TextDisplayModule
from client import Client
from viewport import Viewport
from unit import Unit
from text_box import TextBox
from utils import get_submodules

import log
import re

log = log.logger

class Map(LiveModule, InteractiveModule, TextDisplayModule):
    def __init__(self):
        self._showing = False
        self._maps = []

    def _register_hooks(self, client):
        client.subscribe("get.map", self._hook_get_map)
        client.subscribe("get.map.units", self._hook_get_map_units)
        client.subscribe("get.map.fow", self._hook_get_map_fow)
        client.subscribe("list.maps", self._hook_list_maps)

        client.subscribe("remove.map.fow", self._hook_remove_map_fow)
        client.subscribe("add.map.fow", self._hook_add_map_fow)

        def initial_data_pull():
            client.send({"type": "command", "key": "get.map"})
            client.send({"type": "command", "key": "get.map.fow"})
            client.send({"type": "command", "key": "get.map.units"})

        client.register_connect_hook(initial_data_pull)

    def _hook_get_map(self, response):
        viewer, vp = get_submodules([Viewport])
        data = response["payload"]
        vp.update_features(data["features"])
        vp.update_screen(data["max_y"], data["max_y"])

    def _hook_get_map_fow(self, response):
        log.info("removing map fow")
        viewer, vp = get_submodules([Viewport])
        vp.set_fow(response["payload"])

    def _hook_remove_map_fow(self, response):
        viewer, vp = get_submodules(Viewport)
        vp.remove_fow(response["details"])

    def _hook_add_map_fow(self, response):
        viewer, vp = get_submodules(Viewport)
        vp.add_fow(response["details"])

    def _hook_get_map_units(self, response):
        viewer, vp = get_submodules([Viewport])
        units = [ Unit(unit) for unit in response["payload"] ]
        vp.update_units(units)



    def _update(self, viewer, hashes):
        pass

    def _handle(self, viewer, ch):
        pass

    def _handle_help(self, viewer, buf):
        pass

    def _handle_combo(self, viewer, buf):
        split = buf.split(" ")
        if split[0] == "map" or split[0] == "m" or split[0] == "maps":
            self._show(viewer)

            if len(split) == 1 :
                pass

            elif len(split) == 4 and (split[1] == "move" or split[1] == "m"):
                from users import Users
                viewer, users = get_submodules(Users)

                regex = split[2]
                map_to_switch = split[3]

                valid_map = False
                for map_name in self._maps:
                    if map_name == map_to_switch:
                        valid_map = True
                        break
                log.error("valid map {0}".format(valid_map))

                if valid_map:

                    usernames = [ user["username"] for user in users.users ]

                    if len(regex) == 1 and regex == "*":
                        regex = ".*"
                    log.error(regex)
                    regex = re.compile(regex)
                    filtered_usernames = list(filter(regex.match, usernames))
                    log.error(filtered_usernames)

                    client = viewer.get_submodule(Client)

                    for username in usernames:
                        v = get_submodules()
                        v.client.send({
                            "type": "command",
                            "key": "move.user",
                            "details": {
                                "username": username,
                                "map_name": map_to_switch
                            }
                        })

            elif len(split) == 5 and (split[1] == "new" or split[1] == "n"):
                name = split[2]
                width = split[3]
                height = split[4]

                try:
                    width = int(width)
                    height = int(height)
                except ValueError:
                    return

                viewer = get_submodules()
                viewer.client.send({
                    "type": "command",
                    "key": "add.map",
                    "details": {
                        "name": name,
                        "width": width,
                        "height": height
                    }
                })

    def _show(self, viewer):
        viewer.apply_to_submodules(TextDisplayModule, lambda x: x._hide(viewer))
        self._showing = True
        self.list_maps()

    def _hide(self, viewer):
        self._showing = False

    def _hook_list_maps(self, response):
        self._maps = response["payload"]

        if self._showing:
            self.show_maps()

    def list_maps(self):
        viewer = get_submodules()
        data = viewer.client.send({
            "type": "command",
            "key": "list.maps"
        })


    def show_maps(self):
        log.info("Showing maps")

        from users import Users
        viewer, tb, users = get_submodules([TextBox, Users])

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



