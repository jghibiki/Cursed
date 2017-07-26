from interactive import  InteractiveModule, LiveModule, TextDisplayModule
from text_box import TextBox
from client import Client
from map import Map
from utils import get_submodules
import log

log = log.logger

class Users(InteractiveModule, LiveModule, TextDisplayModule):
    def __init__(self):
        self._showing = False
        self.users = []

        self._previous_hash = None


    def _update(self, viewer, hashes):
        pass

    def _handle(self, viewer, ch):
        if ch == ord("U"):
            viewer.apply_to_submodules(TextDisplayModule, lambda x: x._hide(viewer))
            self._show()

    def _handle_combo(self, viewer, buff):
        pass

    def _handle_help(self, viewer, buf):
        pass

    def _show(self):
        log.info("Showing users.")
        self._showing = True
        viewer = get_submodules()
        viewer.client.send({ "type": "command", "key": "get.users" })

    def _hide(self, viewer):
        log.info("Hiding users.")
        self._showing = False

    def _hook_get_users(self, response):
        self.users = response["payload"]
        log.info("Recieved {} users.".format(len(self.users)))

        viewer, m, tb = get_submodules([Map, TextBox])

        if m._showing:
            m.show_maps()

        if self._showing:
            lines = [ [{
                "text": "Users:\n",
                "color": "Gold"
                }] ]

            for user in self.users:
                lines.append([ {
                    "text": "{0}({1})".format(user["username"], user["role"].upper()),
                    "color": None
                } ])
            tb.set(lines)

    def get_users(self):
        viewer = get_submodules()
        log.info("Getting users")
        viewer.client.send({ "type": "command", "key": "get.users" })

    def _register_hooks(self, client):
        client.subscribe("get.users", self._hook_get_users)

        def initial_data_pull():
            self.get_users()

        client.register_connect_hook(initial_data_pull)




