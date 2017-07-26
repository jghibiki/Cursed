from interactive import  InteractiveModule, LiveModule, TextDisplayModule
from client import Client
from narrative import Narrative
from state import State
from colon_line import ColonLine
from text_box import TextBox
from users import Users
import log


log = log.logger

class Chat(InteractiveModule, LiveModule, TextDisplayModule):

    def __init__(self):
        self._username = None
        self._showing = False
        self._previous_hash = None

    def _update(self, viewer, hashes):
        if self._showing:
            pass #TODO determine relevence of _update

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
                viewer.client.send({
                    "type": "command",
                    "key": "add.chat.message",
                    "details": {
                        "sender": username,
                        "persona": None,
                        "message": ' '.join(buff[1:]),
                        "recipient": None
                    }
                })


                viewer.client.send({"type": "command", "key": "get.chat"})
            else:
                cl = viewer.get_submodule(ColonLine)
                cl.set_msg("No username set. Set one with :set username <username>")

        elif ( ( buff[0] == "whisper" or buff[0] == "w" ) and
                 len(buff) > 2 ):
            username = state.get_state("username")
            viewer.apply_to_submodules(TextDisplayModule, lambda x: x._hide(viewer))

            if username:
                viewer.client.send({
                    "type": "command",
                    "key": "add.chat.message",
                    "details": {
                        "sender": username,
                        "persona": None,
                        "message": ' '.join(buff[2:]),
                        "recipient": buf[1]
                    }
                })

                viewer.client.send({"type": "command", "key": "get.chat"})

            else:
                cl = viewer.get_submodule(ColonLine)
                cl.set_msg("No username set. Set one with :set username <username>")

        elif ( ( buff[0] == "impersonate" or buff[0] == "imp" ) and
                 len(buff) > 2 ):
            username = state.get_state("username")
            viewer.apply_to_submodules(TextDisplayModule, lambda x: x._hide(viewer))

            if username:

                viewer.client.send({
                    "type": "command",
                    "key": "add.chat.message",
                    "details": {
                        "sender": username,
                        "persona": buff[1],
                        "message": ' '.join(buff[2:]),
                        "recipient": None
                    }
                })

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
            viewer.client.send({"type": "command", "key": "get.chat"})

        else:
            cl = viewer.get_submodule(ColonLine)
            cl.set_msg("No username set. Set one with :set username <username>")


    def _hook_get_chat(self, response):
        import viewer
        viewer = viewer.Viewer.instance
        tb = viewer.get_submodule(TextBox)
        u = viewer.get_submodule(Users)
        state = viewer.get_submodule(State)
        username = state.get_state("username")
        log.info("updating_chat")

        messages = response["payload"]

        gm_user = None
        for user in u.users:
            if user["role"] == "gm":
                gm_user = user["username"]
                break
        log.error(u.users)

        lines = [ [{
            "text": "Chat:\n",
            "color": "Gold"
            }] ]

        for message in messages:
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
            elif message["persona"] is not None:
                log.error(gm_user)
                if message["sender"] == gm_user:
                    line = [
                        {
                            "text": "{0} <{1}>: ".format(message["persona"], message["sender"]),
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
                            "text": "{0} <{1}>: ".format(message["persona"], message["sender"]),
                            "color": "Grey"
                        },
                        {
                            "text": message["message"],
                            "color": None
                        }
                    ]
            else:
                if message["sender"] == gm_user:
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
        tb.set(lines)


    def _hide(self, viewer):
        self._showing = False


    def _register_hooks(self, client):
        import viewer
        viewer = viewer.Viewer.instance
        viewer.client.subscribe("get.chat", self._hook_get_chat)
