from interactive import VisibleModule, InteractiveModule
from features import FeatureType
from viewer import ViewerConstants
import curses
import logging

log = logging.getLogger('simple_example')


class StatusLine(VisibleModule):

    def __init__(self, max_y, max_x):
        self.initial_draw_priority = 99
        self.draw_priority = 99

        self.x = 0
        self.y = ViewerConstants.max_y-2
        self.h = 3
        self.w = max_x

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
            if force: log.debug("status_line.draw forced")

            padded_ln1 = self._buffer.ljust(ViewerConstants.max_x)
            padded_ln2 = self._msg.ljust(ViewerConstants.max_x)
            self._screen.addstr(0,0, "▒"*ViewerConstants.max_x, curses.color_pair(179))
            self._screen.addstr(1,0, padded_ln1, curses.color_pair(179))
            self._screen.addstr(2,0, padded_ln2)

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
