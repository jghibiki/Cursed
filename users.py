from interactive import  InteractiveModule, LiveModule, TextDisplayModule
from text_box import TextBox
from client import Client
import logging

log = logging.getLogger('simple_example')

class Users(InteractiveModule, LiveModule, TextDisplayModule):
    def __init__(self):
        self._showing = False
        self.users = []


    def _update(self, viewer, hashes):
        pass

    def _handle(self, viewer, ch):
        if ch == ord("U"):
            viewer.apply_to_submodules(TextDisplayModule, lambda x: x._hide(viewer))
            self._show(viewer)

    def _handle_combo(self, viewer, buff):
        pass

    def _handle_help(self, viewer, buf):
        pass

    def _show(self, viewer):
        self._showing = True

        c = viewer.get_submodule(Client)
        tb = viewer.get_submodule(TextBox)
        self._get_users(viewer)

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


    def _hide(self, viewer):
        self._showing = False


    def _get_users(self, viewer):

        tb = viewer.get_submodule(TextBox)
        c = viewer.get_submodule(Client)
        data = c.make_request("/users")
        self.users = data["users"]


