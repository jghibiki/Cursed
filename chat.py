from interactive import  InteractiveModule
from client import Client
from narrative import Narrative
from state import State
from status_line import StatusLine
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
        if ( len(buff) > 1 and
             buff[0] == "c" or
             buff[0] == "chat" ):

            username = state.get_state("username")
            if username:
                if buff[1] == "view" or buff[1] == "v":

                        c = viewer.get_submodule(Client)
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

                elif ( ( buff[1] == "send" or buff[1] == "s" ) and
                         len(buff) > 2 ):
                    username = state.get_state("username")

                    if username:
                        c = viewer.get_submodule(Client)
                        data = c.make_request("/chat", payload={
                            "sender": username,
                            "recipient": None,
                            "message": ' '.join(buff[2:])
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

                elif ( ( buff[1] == "whisper" or buff[1] == "w" ) and
                         len(buff) > 3 ):
                    username = state.get_state("username")

                    if username:
                        c = viewer.get_submodule(Client)
                        data = c.make_request("/chat", payload={
                            "sender": username,
                            "recipient": buff[2],
                            "message": ' '.join(buff[3:])
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
                sl = viewer.get_submodule(StatusLine)
                sl.set_msg("No username set. Set one with :set username <username>")


    def _handle_help(self, viewer, buf):
        pass



