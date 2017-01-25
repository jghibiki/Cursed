import curses
import curses.textpad
import os
from viewer import ViewerConstants
from interactive import VisibleModule, InteractiveModule
from viewport import Viewport
from colon_line import ColonLine
from screen import Screen
from status_line import StatusLine
from client import Client
import math
import logging

log = logging.getLogger('simple_example')


class Editor(VisibleModule, InteractiveModule):

    def __init__(self):


        self.initial_draw_priority = 5
        self.draw_priority = 5

        self.x = 0
        self.y = 0
        self.h = 1
        self.w = 2

        self._dirty = True
        self._screen = curses.newpad(self.h, self.w)



    def draw(self, viewer, force=False):
        if self._dirty or force:
            self._dirty = False
            return True
        return False


    def _handle_combo(self, viewer, buf):
        pass



    def _handle(self, viewer, ch):

        vp = viewer.get_submodule(Viewport)
        screen = viewer.get_submodule(Screen)
        sl = viewer.get_submodule(StatusLine)
        c = viewer.get_submodule(Client)

        # show help
        if ch == ord("?"):
            help_text = """DM Tools Editor Help:
Controls:
<spacebar> : Add feature at cursor
         x : Remove feature at cursor
         j : move cursor down
         k : move cursor up
         h : move cursor left
         l : move cursor right
         B : Block fill. Press once to set first corner. Move cursor and press again to set the second corner of the block.
         X : Block remove. Press once to set first corner. Move cursor and press again to set second corner of the block.
         J : Move view port down
         K : Move view port up
         H : Move view port left
         L : Move view port right
    Ctrl+G : Close text box
         n : View/Edit notes on feature. Features with notes will flash.

Feature Types:
         w : Wall(brown ▒)
         W : Water(Blue ~)
         d : Door(D)
         G : Gate(G)
         r : Road(Grey ▒)
         o : Bush(Green o)
         . : Grass(Green .)
         t : Table(┬)
         c : Chair(c)
         T : Tree(Brown O)
         ^ : Elevated ground(^)
         > : Up StairLadder(↑)
         < : Down Stair/Ladder(↓)
         % : Lantern(Yellow %)
         # : Chest(#)

 ** Ctrl+G to Exit **
                """
            textbox = viewer.make_textbox(5, 5, self.max_y-10, self.max_x-10, deco="frame", value=help_text)
            textbox.edit()
            del textbox # explicitly dispose
            viewer._dirty = True


    def right(self):
        if self.w - self.x > ViewerConstants.max_x-1:
            self.x += 1
            self._dirty = True

    def down(self):
        if (self.h - self.y) > ViewerConstants.max_y-2:
            self.y += 1
            self._dirty = True

    def up(self):
        if self.y-1 >= 0:
            self.y -= 1
            self._dirty = True

    def left(self):
        if self.x-1 >= 0:
            self.x -= 1
            self._dirty = True
