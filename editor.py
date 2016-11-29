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


class Editor(VisibleModule, InteractiveModule):

    def __init__(self, max_y, max_x):

        self.x_block = None
        self.block = None

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
        # TODO: Fix overlaying
        #vp = viewer.get_submodule(Viewport)
        #if self.block:
        #    vp._screen.addstr(self.block[0], self.block[1], "B", curses.A_BLINK)
        #if self.x_block:
        #    vp._screen.addstr(self.x_block[0], self.x_block[1], "X", curses.A_BLINK)

        #self._screen.noutrefresh(
        #        self.y,
        #        self.x,
        #        1,0,
        #        ViewerConstants.max_y,
        #        ViewerConstants.max_x)

        self._dirty = False
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
            feature = Feature(screen.y - 1 + vp.y,
                              screen.x + vp.x,
                              self.current_obj)
            raw_feature = FeatureSerializer.toDict(feature)
            c.make_request("/map/add", payload=raw_feature)

            # TODO: remove below
            #vp.add_feature(
            #        screen.y - 1 + vp.y,
            #        screen.x + vp.x,
            #        self.current_obj)
            screen.fix_cursor()

        # remove feature
        elif ch == ord("x"):
            c.make_request("/map/rm", payload={
                "y": screen.y - 1 + vp.y,
                "x": screen.x + vp.x
            })
            #vp.rm_feature(
            #        screen.y - 1 + vp.y,
            #        screen.x + vp.x)
            screen.fix_cursor()

        # edit/view note

        # add block
        elif ch == ord("b"):
            if not self.block:
                self.block = (screen.y + vp.y,
                              screen.x + vp.x)
                self._dirty = True
            else:
                yx2 = (screen.y + vp.y,
                       screen.x + vp.x)


                if self.block[0] == yx2[0] and self.block[1] == yx2[1]:
                    vp.add_feature(
                            yx2[0]-1,
                            yx2[1],
                            self.current_obj)
                    self._dirty = True

                else:
                    y_max = max([self.block[0], yx2[0]])
                    y_min = min([self.block[0], yx2[0]])

                    x_max = max([self.block[1], yx2[1]])
                    x_min = min([self.block[1], yx2[1]])

                    y_diff = (y_max - y_min) + 1
                    x_diff = (x_max - x_min) + 1


                    for y in range(y_diff):
                        for x in range(x_diff):
                            vp.add_feature(
                                    y+y_min-1,
                                    x+x_min,
                                    self.current_obj)

                    screen.move_cursor(screen.y, screen.x)
                self._dirty = True
                self.block = None

        # remove block
        elif ch == ord("X"):
            if not self.x_block:
                self.x_block = (screen.y + vp.y,
                                screen.x + vp.x)
                self._dirty = True
            else:
                yx2 = (screen.y + vp.y,
                       screen.x + vp.x)


                if self.x_block[0] == yx2[0] and self.x_block[1] == yx2[1]:
                    vp.add_feature(
                            yx2[0]-1,
                            yx2[1],
                            self.current_obj)
                    self._dirty = True

                else:
                    y_max = max([self.x_block[0], yx2[0]])
                    y_min = min([self.x_block[0], yx2[0]])

                    x_max = max([self.x_block[1], yx2[1]])
                    x_min = min([self.x_block[1], yx2[1]])

                    y_diff = (y_max - y_min) + 1
                    x_diff = (x_max - x_min) + 1


                    for y in range(y_diff):
                        for x in range(x_diff):
                            vp.rm_feature(
                                    y+y_min-1,
                                    x+x_min)

                    screen.move_cursor(screen.y, screen.x)
                self._dirty = True
                self.x_block = None

        elif ch == 27: # escape
            if self.block:
                self.block = None
                self._dirty = True
            if self.x_block:
                self.x_block = None
                self._dirty = True


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
