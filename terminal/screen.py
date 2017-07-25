from interactive import VisibleModule
from viewport import Viewport
from viewer import ViewerConstants
import curses
import log
import math

log = log.logger

class Screen(VisibleModule):
    def __init__(self, screen):
        self.screen = screen

        self.initial_draw_priority = 100
        self.draw_priority = -100

        self.y = int(ViewerConstants.max_y/2)
        self.x = math.floor(ViewerConstants.max_x/3) + math.floor(math.floor(ViewerConstants.max_x/2)/2)

        self._dirty = True

    def draw(self, viewer, force=False):
        from editor import Editor
        editor = viewer.get_submodule(Editor)
        if self._dirty or force:
            if force: log.debug("screen.draw forced")

            self.screen.move(self.y, self.x)
            self.screen.noutrefresh()
            self._dirty = False
            return True
        return False


    def up(self):
        self.y -= 1
        self.screen.move(self.y, self.x)
        self._dirty = True

    def down(self):
        self.y += 1
        self.screen.move(self.y, self.x)
        self._dirty = True

    def left(self):
        self.x -= 1
        self.screen.move(self.y, self.x)
        self._dirty = True

    def right(self):
        self.x += 1
        self.screen.move(self.y, self.x)
        self._dirty = True

    def fix_cursor(self):
        self.screen.move(self.y, self.x)
        self.screen.cursyncup()
        self._dirty = True

    def move_cursor(self, y, x):
        self.y = y
        self.x = x
        self.screen.move(self.y, self.x)
        self._dirty = True

    def make_textbox(self, y, x, h, w, value="", deco=None, text_color_pair=0, deco_color=0):
        nw = curses.newwin(h, w, y, x)
        txtbox = curses.textpad.Textbox(nw)
        if deco == "frame":
            self.screen.attron(deco_color)
            curses.textpad.rectangle(self.screen, y-1, x-1, y+h, x+w)
            self.screen.attroff(deco_color)
        elif deco == "underline":
            self.screen.hline(y+1, x, curses.ACS_HLINE, deco_color)

        nw.addstr(0,0,value,text_color_pair)
        nw.attron(text_color_pair)
        self.screen.refresh()
        return txtbox
