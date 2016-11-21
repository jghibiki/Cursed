from features import Feature, FeatureType, FeatureSerializer
from interactive import VisibleModule
from viewport import Viewport
from viewer import ViewerConstants
import curses

class Screen(VisibleModule):
    def __init__(self, screen):
        self.screen = screen

        self.draw_priority = 0

        self.y = int(ViewerConstants.max_y/2)
        self.x = int(ViewerConstants.max_x/2)

        self._dirty = True

        self.current_obj = "Wall"

    def draw(self, viewer):
        if self._dirty:
            vp = viewer.get_submodule(Viewport)
            self.set_status_line(
                    "CUR(%s, %s), VP(%s, %s), MODE(%s)" %
                    (self.y,
                        self.x,
                        vp.y,
                        vp.x,
                        FeatureType.toName(self.current_obj)))

            self.screen.move(self.y, self.x)
            self.screen.noutrefresh()
            return True
        return False

    def set_status_line(self, msg):
        """ This should probably be refactored out"""
        padded = msg.ljust(ViewerConstants.max_x)
        self.screen.addstr(0,0, padded)

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
