import curses
import curses.textpad
import os
from features import Feature, FeatureType, FeatureSerializer
from viewer import ViewerConstants
from interactive import VisibleModule, InteractiveModule
from viewport import Viewport
from status_line import StatusLine
from screen import Screen
from client import Client
import math
import logging

log = logging.getLogger('simple_example')


class Editor(VisibleModule, InteractiveModule):

    def __init__(self, max_y, max_x):


        self.initial_draw_priority = 5
        self.draw_priority = 5

        self.x = 0
        self.y = 0
        self.h = max_y + 1
        self.w = max_x + 2

        self._dirty = True
        self._screen = curses.newpad(self.h, self.w)

        self.current_obj = FeatureType.wall


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
        # detect place object
        if ch == ord(" "):
            feature = Feature(vp.cursor_y,
                              vp.cursor_x,
                              self.current_obj)
            raw_feature = FeatureSerializer.toDict(feature)
            c.make_request("/map/add", payload=raw_feature)

        # remove feature
        elif ch == ord("x"):
            c.make_request("/map/rm", payload={
                "y": vp.cursor_y,
                "x": vp.cursor_x
            })


        # catch object type
        elif ch == ord("c"):
            self.current_obj = FeatureType.chair
            sl.mark_dirty()
            self._dirty = True

        elif ch == ord("d"):
            self.current_obj = FeatureType.door
            sl.mark_dirty()
            self._dirty = True

        elif ch == ord("w"):
            self.current_obj = FeatureType.wall
            sl.mark_dirty()
            self._dirty = True

        elif ch == ord("t"):
            self.current_obj = FeatureType.table
            sl.mark_dirty()
            self._dirty = True

        elif ch == ord(">"):
            self.current_obj = FeatureType.up_stair
            sl.mark_dirty()
            self._dirty = True

        elif ch == ord("<"):
            self.current_obj = FeatureType.down_stair
            sl.mark_dirty()
            self._dirty = True

        elif ch == ord("%"):
            self.current_obj = FeatureType.lantern
            sl.mark_dirty()
            self._dirty = True

        elif ch == ord("#"):
            self.current_obj = FeatureType.chest
            sl.mark_dirty()
            self._dirty = True

        elif ch == ord("*"):
            self.current_obj = FeatureType.point_of_interest
            sl.mark_dirty()
            self._dirty = True

        elif ch == ord("r"):
            self.current_obj = FeatureType.road
            sl.mark_dirty()
            self._dirty = True

        elif ch == ord("G"):
            self.current_obj = FeatureType.gate
            sl.mark_dirty()
            self._dirty = True

        elif ch == ord("W"):
            self.current_obj = FeatureType.water
            sl.mark_dirty()
            self._dirty = True

        elif ch == ord("T"):
            self.current_obj = FeatureType.tree
            sl.mark_dirty()
            self._dirty = True

        elif ch == ord("o"):
            self.current_obj = FeatureType.bush
            sl.mark_dirty()
            self._dirty = True

        elif ch == ord("."):
            self.current_obj = FeatureType.grass
            sl.mark_dirty()
            self._dirty = True

        elif ch == ord(","):
            self.current_obj = FeatureType.friendly_unit
            sl.mark_dirty()
            self._dirty = True

        elif ch == ord("@"):
            self.current_obj = FeatureType.enemy_unit
            sl.mark_dirty()
            self._dirty = True

        elif ch == ord("$"):
            self.current_obj = FeatureType.dead_unit
            sl.mark_dirty()
            self._dirty = True

        elif ch == ord("^"):
            self.current_obj = FeatureType.hill
            sl.mark_dirty()
            self._dirty = True

        # show help
        elif ch == ord("?"):
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
