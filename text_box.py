from interactive import VisibleModule, InteractiveModule, TextDisplayModule
from viewer import ViewerConstants
from client import Client
from state import State
import colors
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
        self._default_lines = [
                [
                    {
                        "text": "Text Box:" ,
                        "color": "Gold"
                    }
                ],
                [
                    {
                        "text": "ctrl + j",
                        "color": "Gold"
                    },
                    {
                        "text": " - scroll down",
                        "color": None
                    }
                ],
                [
                    {
                        "text": "ctrl + k" ,
                        "color": "Gold"
                    },
                    {
                        "text": " - scroll up",
                        "color": None
                    }
                ],
                [
                    {
                        "text": ":clear",
                        "color": "Gold"
                    },
                    {
                        "text": " - clear text box.",
                        "color": None
                    }

                ],
                [
                    {
                        "text": ":read",
                        "color": "Gold"
                    },
                    {
                        "text": " - read text in window. GM only.",
                        "color": None
                    }
                ],
                [
                    {
                        "text":  "Narrative (GM Only):",
                        "color": "Gold"
                    }
                ],
                [
                    {
                        "text": ":n list",
                        "color": "Gold"
                    },
                    {
                        "text": " - list chapters.",
                        "color": None
                    }
                ],
                [
                    {
                        "text": ":n view <chapter number>",
                        "color": "Gold"
                    },
                    {
                        "text": " - view chapter.",
                        "color": None
                    }
                ],
                [
                    {
                        "text": ":n edit <chapter number>",
                        "color": "Gold"
                    },
                    {
                        "text": " - edit chapter.",
                        "color": None
                    }
                ],
                [
                    {
                        "text": ":n read <chapter number>",
                        "color": "Gold"
                    },
                    {
                        "text": ": - read chapter. requires espeak.",
                        "color": None
                    }
                ],
                [
                    {
                        "text": "Chat:",
                        "color": "Gold"
                    }
                ],
                [
                    {
                        "text": ":chat <message>",
                        "color": "Gold"
                    },
                    {
                        "text": " - send a message to all players",
                        "color": None
                    }
                ],
                [
                    {
                        "text": ":whisper <username> <message>",
                        "color": "Gold"
                    },
                    {
                        "text": " - send a message to a specific player",
                        "color": None
                    }
                ]
        ]

        self._lines = self._default_lines
        self._previous_lines = []
        self._page = 0
        self._max_text_w = self.w - 2
        self._max_text_h = self.h - 2

        self._dirty = True

    def draw(self, viewer, force=False):
        if self._dirty or force:
            if force: log.debug("narrative.draw forced")
            self._screen.erase()

            state = viewer.get_submodule(State)
            self._screen.attrset(colors.get("Gold"))

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
            self._screen.attroff(colors.get("Gold"))


            offset_width = self._max_text_w
            line_no = 1
            for line in self._lines:
                char = 2

                for part in line:

                    for text in part["text"]:

                        if char == offset_width:
                            char = 2
                            line_no += 1

                        if part["color"]:
                            self._screen.addstr(line_no, char, text, colors.get(part["color"]))
                        else:
                            self._screen.addstr(line_no, char, text)
                        char += len(text)

                line_no += 1



            #self._paged_text = []
            #for line in self._text.splitlines():
            #    splits = [ line[i:i+self._max_text_w] for i in range(0, len(line), self._max_text_w) ]
            #    self._paged_text = self._paged_text + (splits if splits else [""])

            #x = 0
            #page = 0
            #for line in self._paged_text:
            #    if page >= self._page:
            #        self._screen.addstr(x+1, 2, line)
            #        x += 1
            #    if x > self._max_text_h-1:
            #        break
            #    page += 1


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
                self.set(self._previous_lines)

        elif buff[0] == "clear":
            viewer.apply_to_submodules(TextDisplayModule, lambda x: x._hide(viewer))
            self.set(self._default_lines)
            self._dirty = True

        elif buff[0] == "read" and len(buff) == 1:
            state = viewer.get_submodule(State)
            if state.get_state("role") == "gm":
                import subprocess
                import os
                text = self._paged_text

                FNULL = open(os.devnull, 'w')
                for line in text:
                    try: # lazily handle failure
                        subprocess.call(["espeak", line], stdout=FNULL, stderr=subprocess.STDOUT)
                    except:
                        pass

    def _handle_help(self, viewer, buff):
        pass

    def set_text(self, text):
        raise Exception()

    def set(self, lines):
        self._previous_lines = self._lines
        self._lines = lines
        self._page = 0
        self._dirty = True




    def get_text(self):
        return self._text



lines = [
    [ {"color": "Gold", "text": "this is a line of text"}]
]
