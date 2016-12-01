from interactive import VisibleModule, InteractiveModule
from viewer import ViewerConstants
from client import Client
from state import State
import logging
import math
import curses


log = logging.getLogger('simple_example')

class TextBox(VisibleModule, InteractiveModule):

    def __init__(self):
        self.initial_draw_priority = -1
        self.draw_priority = 10

        self.x = 0
        self.y = 0
        self.h = ViewerConstants.max_y-2
        self.w = math.floor(ViewerConstants.max_x/3)

        self._screen = curses.newwin(self.h, self.w, self.y, self.x)
        self._default_text = ("Text Box: \n" +
                              "ctrl + j - scroll down\n" +
                              "ctrl + k - scroll up\n" +
                              ":clear - clear text box.\n" +
                              ":read - read text in window.\n"
                              "\nNarrative:\n" +
                              ":n list - list chapters.\n" +
                              ":n view <chapter number> - view chapter.\n" +
                              ":n edit <chapter number> - edit chapter.\n" +
                              ":n read <chapter number> - read chapter. requires espeak.\n" +
                              "\nChat:\n" +
                              ":send <message> - send a message to all players\n" +
                              ":whisper <username> <message> - send a message to a specific player\n"
                              )
        self._previous_text = None
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

            state = viewer.get_submodule(State)
            self._screen.attrset(curses.color_pair(179))

            if state.get_state("easter_egg") is not None:
                self._screen.border(
                        curses.ACS_VLINE,
                        curses.ACS_VLINE,
                        curses.ACS_HLINE,
                        curses.ACS_HLINE,
                        curses.ACS_DIAMOND,
                        curses.ACS_DIAMOND,
                        curses.ACS_DIAMOND,
                        curses.ACS_DIAMOND
                )
            else:
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
        if buff[0] == "back":
            if self._previous:
                self.set_text(self._previous)

        elif buff[0] == "read" or buff[0] == "r" and len(buff) == 1:
            import subprocess
            import os
            text = self._paged_text

            FNULL = open(os.devnull, 'w')
            for line in text:
                try: # lazily handle failure
                    subprocess.call(["espeak", line], stdout=FNULL, stderr=subprocess.STDOUT)
                except:
                    pass

    def set_text(self, text):
        self._previous_text = self._text
        self._text = text
        self._page = 0
        self._dirty = True

    def get_text(self):
        return self._text
