from interactive import VisibleModule, InteractiveModule
from viewer import ViewerConstants
from state import State
import colors
import curses
import logging
import math

log = logging.getLogger('simple_example')


class ColonLine(VisibleModule):

    def __init__(self):
        self.initial_draw_priority = 99
        self.draw_priority = 99
        self.x = 0
        self.y = ViewerConstants.max_y-2
        self.h = 3
        self.w = math.floor(curses.COLS/2)+1

        self._buffer = ""
        self._msg = ""
        self._dirty = True
        self._screen = curses.newwin(self.h, self.w, self.y, self.x)


    def draw(self, viewer, force=False):
        from editor import Editor
        from screen import Screen
        from viewport import Viewport
        editor = viewer.get_submodule(Editor)
        screen = viewer.get_submodule(Screen)
        vp = viewer.get_submodule(Viewport)

        if self._dirty or force:
            if force: log.debug("colon_line.draw forced")

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
                        curses.ACS_VLINE,
                        curses.ACS_VLINE,
                        curses.ACS_HLINE,
                        curses.ACS_HLINE,
                        curses.ACS_ULCORNER,
                        curses.ACS_URCORNER,
                        curses.ACS_LLCORNER,
                        curses.ACS_LRCORNER,
                )
            self._screen.attroff(colors.get("Gold"))

            if self._msg != "":
                padded_ln = self._msg.ljust(self.w-2)
            else:
                padded_ln = self._buffer.ljust(self.w-2)
            self._screen.addstr(1,1, padded_ln, colors.get("Gold"))

            self._msg = ""

            self._screen.noutrefresh()

            self._dirty = False
            return True
        return False

    def mark_dirty(self):
        self._dirty = True

    def set_buff(self, buff):
        self._buffer = buff
        self._dirty = True

    def clear_buff(self):
        self._buffer = ""
        self._dirty = True

    def set_msg(self, msg):
        self._msg = msg
        self._dirty = True

    def clear_msg(self):
        self._msg = ""
        self._dirty = True
