from interactive import VisibleModule
from features import FeatureType
from viewer import ViewerConstants
import curses


class StatusLine(VisibleModule):

    def __init__(self, max_y, max_x):
        self.initial_draw_priority = 99
        self.draw_priority = 99

        self.x = 0
        self.y = 0
        self.h = 1
        self.w = max_x

        self._dirty = True
        self._screen = curses.newpad(self.h, self.w)


    def draw(self, viewer, force=False):
        from editor import Editor
        from screen import Screen
        from viewport import Viewport
        editor = viewer.get_submodule(Editor)
        screen = viewer.get_submodule(Screen)
        vp = viewer.get_submodule(Viewport)

        if self._dirty or force:
            if force: log.debug("status_line.draw forced")
            if editor:
                self.set_status_line(
                        "CUR(%s, %s), VP(%s, %s), MODE(%s)" %
                        (screen.y,
                            screen.x,
                            vp.y,
                            vp.x,
                            FeatureType.toName(editor.current_obj)))
            else:
                self.set_status_line(
                        "CUR(%s, %s), VP(%s, %s)" %
                        (self.y,
                            self.x,
                            vp.y,
                            vp.x))

            self._screen.noutrefresh(
                    self.y,
                    self.x,
                    0,0,
                    ViewerConstants.max_y,
                    ViewerConstants.max_x)

            self._dirty = False
            return True
        return False


    def set_status_line(self, msg):
        """ This should probably be refactored out"""
        padded = msg.ljust(ViewerConstants.max_x)
        self._screen.addstr(0,0, padded)

    def mark_dirty(self):
        self._dirty = True
