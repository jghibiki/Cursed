from interactive import VisibleModule, InteractiveModule, TextDisplayModule
from viewer import ViewerConstants
from client import Client
from text_box import TextBox
import logging
import curses
import math
import sys, tempfile, os
import subprocess

log = logging.getLogger('simple_example')


class Narrative(InteractiveModule, TextDisplayModule):

    def __init__(self):
        self._showing = False


    def _handle(self, viewer, ch):
        pass

    def _handle_combo(self, viewer, buff):
        tb = viewer.get_submodule(TextBox)

        buff = buff.split(" ")
        if ( len(buff) > 1 and
             buff[0] == "n" or
             buff[0] == "narrative"):

            if buff[1] == "list" or buff[1] == "l":
                c = viewer.get_submodule(Client)
                viewer.apply_to_submodules(TextDisplayModule, lambda x: x._hide(viewer))
                data = c.make_request("/narrative")
                lines = [
                    [
                        {
                            "text": "Chapters",
                            "color": "Gold"
                        }
                    ]
                ]
                text = ""
                for idx, chapter in enumerate(data["chapters"]):
                    text += ("%02d. %s\n" % (idx+1, chapter))
                for line in text.split("\n"):
                    lines.append([
                        {
                            "text": line,
                            "color": None
                        } ])
                tb.set(lines)

                self._dirty = True

            elif ( ( buff[1] == "view" or buff[1] == "v" ) and
                   len(buff) == 3 ):
                c = viewer.get_submodule(Client)
                viewer.apply_to_submodules(TextDisplayModule, lambda x: x._hide(viewer))
                if buff[2] != "":
                    bad_int = False
                    try:
                        int(buff[2])
                    except:
                        bad_int = True
                    if not bad_int:
                        data = c.make_request("/narrative/%s" % (int(buff[2])-1))

                        lines = []
                        for line in data["text"].split("\n"):
                            lines.append([
                                {
                                    "text": line,
                                    "color": None
                                } ])
                        tb.set(lines)

                    self._dirty = True

            elif ( ( buff[1] == "edit" or buff[1] == "e" ) and
                    len(buff) == 3 ):
                c = viewer.get_submodule(Client)
                viewer.apply_to_submodules(TextDisplayModule, lambda x: x._hide(viewer))
                id = (int(buff[2])-1)
                data = c.make_request("/narrative/%s" % id)
                text = data["text"]


                EDITOR = os.environ.get('EDITOR','vim')
                with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
                    text = text.encode("UTF-8")
                    tf.write(text)
                    tf.flush()
                    subprocess.call([EDITOR, tf.name])

                    # do the parsing with `tf` using regular File operations.
                    # for instance:
                    tf.seek(0)
                    text = tf.read().decode("UTF-8")
                    data["text"] = text

                    # TODO: add a way to upload edited note to server
                    data = c.make_request('/narrative/%s' % id, payload=data)
                    lines = []
                    for line in text.split("\n"):
                        lines.append([
                            {
                                "text": line,
                                "color": None
                            } ])
                    tb.set(lines)

                    # fix cursor mode
                    curses.curs_set(1)
                    curses.curs_set(0)
                viewer._draw(force=True) # force redraw after closing vim


            elif buff[1] == "read" or buff[1] == "r":
                text = ""

                c = viewer.get_submodule(Client)
                viewer.apply_to_submodules(TextDisplayModule, lambda x: x._hide(viewer))
                id = (int(buff[2])-1)
                data = c.make_request("/narrative/%s" % id)
                text = data["text"].splitlines()

                FNULL = open(os.devnull, 'w')
                for line in text:
                    try: # lazily handle failure
                        subprocess.call(["espeak", line], stdout=FNULL, stderr=subprocess.STDOUT)
                    except:
                        pass


    def _handle_help(self, viewer, buff):
        pass

    def _show(self, viewer):
        self._showing = True
        tb = viewer.get_submodule(TextBox)

        c = viewer.get_submodule(Client)
        data = c.make_request("/narrative")
        text = "Chapters:\n"
        for idx, chapter in enumerate(data["chapters"]):
            text += ("%02d. %s\n" % (idx+1, chapter))

        lines = []
        for line in text.split("\n"):
            lines.append([
                {
                    "text": line,
                    "color": None
                } ])
        tb.set(lines)


    def _hide(self, viewer):
        self._showing = False


