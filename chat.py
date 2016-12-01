from interactive import  InteractiveModule
from client import Client
from narrative import Narrative
from state import State
from colon_line import ColonLine
from text_box import TextBox
import logging

log = logging.getLogger('simple_example')

class Chat(InteractiveModule):

    def __init__(self):
        self._username = None

    def _handle(self, viewer, ch):
        pass

    def _handle_combo(self, viewer, buff):
        tb = viewer.get_submodule(TextBox)
        state = viewer.get_submodule(State)


        buff = buff.split(" ")

        log.error(buff)
        if ( ( buff[0] == "send" or buff[0] == "s" ) and
                 len(buff) > 1 ):
            username = state.get_state("username")

            if username:
                c = viewer.get_submodule(Client)
                data = c.make_request("/chat", payload={
                    "sender": username,
                    "recipient": None,
                    "message": ' '.join(buff[1:])
                })

                data = c.make_request("/chat/%s" % username)
                text = "Chat:\n"
                for message in data["messages"]:
                    if message["recipient"] is not None:
                        text += ("<private> %s to %s: %s\n" % (
                            message["sender"],
                            message["recipient"],
                            message["message"]))
                    else:
                        text += ("%s: %s\n" % (
                            message["sender"],
                            message["message"]))
                tb.set_text(text)
            else:
                cl = viewer.get_submodule(ColonLine)
                cl.set_msg("No username set. Set one with :set username <username>")

        elif ( ( buff[0] == "whisper" or buff[0] == "w" ) and
                 len(buff) > 2 ):
            username = state.get_state("username")

            if username:
                c = viewer.get_submodule(Client)
                data = c.make_request("/chat", payload={
                    "sender": username,
                    "recipient": buff[1],
                    "message": ' '.join(buff[2:])
                })

                data = c.make_request("/chat/%s" % username)
                text = "Chat:\n"
                for message in data["messages"]:
                    if message["recipient"] is not None:
                        text += ("private %s to %s: %s\n" % (
                            message["sender"],
                            message["recipient"],
                            message["message"]))
                    else:
                        text += ("%s: %s\n" % (
                            message["sender"],
                            message["message"]))
                tb.set_text(text)

            else:
                cl = viewer.get_submodule(ColonLine)
                cl.set_msg("No username set. Set one with :set username <username>")


    def _handle_help(self, viewer, buf):
        pass

    def show(self, viewer):
        state = viewer.get_submodule(State)
        username = state.get_state("username")

        if username:
            c = viewer.get_submodule(Client)
            tb = viewer.get_submodule(TextBox)
            data = c.make_request("/chat/%s" % username)
            text = "Chat:\n"
            for message in data["messages"]:
                if message["recipient"] is not None:
                    text += ("<private> %s to %s: %s\n" % (
                        message["sender"],
                        message["recipient"],
                        message["message"]))
                else:
                    text += ("%s: %s\n" % (
                        message["sender"],
                        message["message"]))
            tb.set_text(text)

        else:
            cl = viewer.get_submodule(ColonLine)
            cl.set_msg("No username set. Set one with :set username <username>")



