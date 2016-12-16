from interactive import VisibleModule, InteractiveModule
from features import FeatureType
from viewer import ViewerConstants
from state import State
from colors import Colors
import curses
import logging
import math

log = logging.getLogger('simple_example')


class StatusLine(VisibleModule):

    def __init__(self):
        self.initial_draw_priority = 99
        self.draw_priority = 99

        self.x = math.floor(curses.COLS/2)+1
        self.y = ViewerConstants.max_y-2
        self.h = 3
        self.w = math.floor(curses.COLS/2)-1

        self._dirty = True
        self._screen = curses.newwin(self.h, self.w, self.y, self.x)

        self._previous_obj_desc = None


    def draw(self, viewer, force=False):
        from editor import Editor
        from screen import Screen
        from viewport import Viewport

        vp = viewer.get_submodule(Viewport)
        obj_desc = vp.get_cursor_focus(viewer)
        if obj_desc != self._previous_obj_desc: # redraw if desc has changed
            self._previous_obj_desc = obj_desc
            self._dirty = True

        if self._dirty or force:
            if force: log.debug("status_line.draw forced")

            editor = viewer.get_submodule(Editor)
            screen = viewer.get_submodule(Screen)
            state = viewer.get_submodule(State)
            self._screen.attrset(Colors.get(Colors.GOLD))

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

            self._screen.attroff(Colors.get(Colors.GOLD))

            msg = "%s" % (obj_desc)
            padded_ln = msg.ljust(self.w-2)
            self._screen.addstr(1,1, padded_ln, Colors.get(Colors.GOLD))



            self._screen.noutrefresh()

            self._dirty = False
            return True
        return False

    def mark_dirty(self):
        self._dirty = True

