from interactive import  InteractiveModule, LiveModule, TextDisplayModule
from client import Client
from narrative import Narrative
from state import State
from colon_line import ColonLine
from text_box import TextBox
from users import Users
import logging


log = logging.getLogger('simple_example')

class Chat(InteractiveModule, LiveModule, TextDisplayModule):

    def __init__(self):
        self._username = None
        self._showing = False
        self._previous_hash = None

    def _update(self, viewer, hashes):
        if self._showing:
            hash = hashes["chat"]

            if hash != self._previous_hash:
                state = viewer.get_submodule(State)
                tb = viewer.get_submodule(TextBox)
                username = state.get_state("username")
                text = self._get_messages(viewer, username)
                tb.set(text)

    def _handle(self, viewer, ch):
        pass

    def _handle_combo(self, viewer, buff):
        tb = viewer.get_submodule(TextBox)
        state = viewer.get_submodule(State)


        buff = buff.split(" ")

        if ( ( buff[0] == "chat" or buff[0] == "c" ) and
                 len(buff) > 1 ):
            username = state.get_state("username")
            viewer.apply_to_submodules(TextDisplayModule, lambda x: x._hide(viewer))

            if username:
                c = viewer.get_submodule(Client)
                data = c.make_request("/chat", payload={
                    "sender": username,
                    "recipient": None,
                    "message": ' '.join(buff[1:])
                })

                text = self._get_messages(viewer, username)
                text = self._get_messages(viewer, username)
                tb.set(text)
            else:
                cl = viewer.get_submodule(ColonLine)
                cl.set_msg("No username set. Set one with :set username <username>")

        elif ( ( buff[0] == "whisper" or buff[0] == "w" ) and
                 len(buff) > 2 ):
            username = state.get_state("username")
            viewer.apply_to_submodules(TextDisplayModule, lambda x: x._hide(viewer))

            if username:
                c = viewer.get_submodule(Client)
                data = c.make_request("/chat", payload={
                    "sender": username,
                    "recipient": buff[1],
                    "message": ' '.join(buff[2:])
                })

                lines = self._get_messages(viewer, username)
                tb.set(lines)

            else:
                cl = viewer.get_submodule(ColonLine)
                cl.set_msg("No username set. Set one with :set username <username>")


    def _handle_help(self, viewer, buf):
        pass

    def _show(self, viewer):
        state = viewer.get_submodule(State)
        username = state.get_state("username")

        if username:
            self._showing = True
            c = viewer.get_submodule(Client)
            tb = viewer.get_submodule(TextBox)
            lines = self._get_messages(viewer, username)
            tb.set(lines)

        else:
            cl = viewer.get_submodule(ColonLine)
            cl.set_msg("No username set. Set one with :set username <username>")


    def _get_messages(self, viewer, username):
        tb = viewer.get_submodule(TextBox)
        c = viewer.get_submodule(Client)
        u = viewer.get_submodule(Users)
        data = c.make_request("/chat/%s" % username)


        gm_user = None
        for user in u.users:
            if user["role"] == "gm":
                gm_user = user["username"]


        lines = [ [{
            "text": "Chat:\n",
            "color": "Gold"
            }] ]

        for message in data["messages"]:
            if message["recipient"] is not None:
                line = [
                    {
                        "text": "<private> {0} to {1}: ".format(message["sender"], message["recipient"]),
                        "color": "Dark Green"
                    },
                    {
                        "text": message["message"],
                        "color": None
                    }
                ]
            elif message["sender"] == gm_user:
                line = [
                    {
                        "text": "{0}: ".format(message["sender"]),
                        "color": "Gold"
                    },
                    {
                        "text": message["message"],
                        "color": None
                    }
                ]
            else:
                line = [
                    {
                        "text": "{0}: ".format(message["sender"]),
                        "color": "Grey"
                    },
                    {
                        "text": message["message"],
                        "color": None
                    }
                ]
            lines.append(line)

        return lines



    def _hide(self, viewer):
        self._showing = False
