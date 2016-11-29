from interactive import VisibleModule, InteractiveModule
from viewer import ViewerConstants
from client import Client
import logging
import curses
import math
import sys, tempfile, os
import subprocess

log = logging.getLogger('simple_example')


class Narrative(VisibleModule, InteractiveModule):

    def __init__(self):
        self.initial_draw_priority = -1
        self.draw_priority = 10

        self.x = 0
        self.y = 0
        self.h = ViewerConstants.max_y-1
        self.w = math.floor(ViewerConstants.max_x/3)

        self._screen = curses.newwin(self.h, self.w, self.y, self.x)
        self._default_text = ("Narrative:\n" +
                              ":n list - list chapters.\n" +
                              ":n view <chapter number> - view chapter.\n" +
                              ":n edit <chapter number> - edit chapter.\n" +
                              ":n read <chapter number> - read chapter. requires espeak.\n" +
                              ":n read - read text in narrative window.\n")
        self._text = self._default_text
        self._page = 0
        self._max_text_w = self.w - 4
        self._max_text_h = self.h - 2
        self._paged_text = []

        self._dirty = True

    def draw(self, viewer, force=False):
        if self._dirty or force:
            if force: log.debug("narrative.draw forced")
            self._screen.clear()
            self._screen.attrset(curses.color_pair(179))
            self._screen.border(
                    curses.ACS_BOARD,
                    curses.ACS_BOARD,
                    curses.ACS_BOARD,
                    curses.ACS_BOARD,
                    curses.ACS_BOARD,
                    curses.ACS_BOARD,
                    curses.ACS_BOARD,
                    curses.ACS_BOARD
            )
            self._screen.attroff(curses.color_pair(179))


            self._paged_text = []
            for line in self._text.splitlines():
                splits = [ line[i:i+self._max_text_w] for i in range(0, len(line), self._max_text_w) ]
                self._paged_text = self._paged_text + (splits if splits else [""])

            x = 0
            page = 0
            for line in self._paged_text:
                if page >= self._page:
                    self._screen.addstr(x+1, 2, line)
                    x += 1
                if x > self._max_text_h-1:
                    break
                page += 1


            self._screen.noutrefresh()
            self._dirty = False
            return True
        return False

    def _handle(self, viewer, ch):
        if curses.keyname(ch) == b'^J':
            if self._page+self._max_text_h < len(self._paged_text):
                self._page += 1
                self._dirty = True

        if curses.keyname(ch) == b'^K':
            if (self._page - 1) >= 0:
                self._page -= 1
                self._dirty = True

    def _handle_combo(self, viewer, buff):
        buff = buff.split(" ")
        if ( len(buff) > 1 and
             buff[0] == "n" ):

            if buff[1] == "list" or buff[1] == "l":
                c = viewer.get_submodule(Client)
                data = c.make_request("/narrative")
                self._text = "Chapters:\n"
                for idx, chapter in enumerate(data["chapters"]):
                    self._text += ("%02d. %s\n" % (idx+1, chapter))

                self._dirty = True

            elif ( ( buff[1] == "view" or buff[1] == "v" ) and
                   len(buff) == 3 ):
                c = viewer.get_submodule(Client)
                data = c.make_request("/narrative/%s" % (int(buff[2])-1))
                self._text = data["text"]

                self._dirty = True

            elif ( ( buff[1] == "edit" or buff[1] == "e" ) and
                    len(buff) == 3 ):
                c = viewer.get_submodule(Client)
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
                    self._text = text
                viewer._draw(force=True) # force redraw after closing vim

            elif buff[1] == "clear" or buff[1] == "c":
                self._text = self._default_text
                self._dirty = True

            elif buff[1] == "read" or buff[1] == "r":
                text = ""
                if len(buff) == 3:
                    c = viewer.get_submodule(Client)
                    id = (int(buff[2])-1)
                    data = c.make_request("/narrative/%s" % id)
                    text = data["text"]
                    text = text.splitlines()
                else:
                    text = self._paged_text

                FNULL = open(os.devnull, 'w')
                for line in text:
                    subprocess.call(["espeak", line], stdout=FNULL, stderr=subprocess.STDOUT)


    def _handle_help(self, viewer, buff):
        pass

