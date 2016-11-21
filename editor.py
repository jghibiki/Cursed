import curses
import curses.textpad
import os
from features import Feature, FeatureType, FeatureSerializer


class Editor:

    def __init__(self, screen, save_handler, min_y=None, min_x=None, max_y=None, max_x=None):

        self.map = map

        self.save_handler = save_handler

        self.x_block = None
        self.block = None

        self.current_obj = FeatureType.wall


    def draw(self):
        if self.block:
            self.default_screen.addch(self.block[0], self.block[1], ord("B"), curses.A_BLINK)
        if self.x_block:
            self.default_screen.addch(self.x_block[0], self.x_block[1], ord("X"), curses.A_BLINK)


    def help(self, parent, buf):
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
        textbox = parent.make_textbox(5, 5, self.max_y-10, self.max_x-10, deco="frame", value=help_text)
        textbox.edit()
        del textbox # explicitly dispose
        parent.mark_dirty()



    def handle(self, viewer, viewport, ch):

            # detect place object
            if ch == ord(" "):
                viewport.add_feature(
                        viewer.cursor_y - 1 + viewport.y,
                        viewer.cursor_x + viewport.x,
                        self.current_obj)

            # remove feature
            elif ch == ord("x"):
                parent.rm_feature(
                        parent.cursor_y - 1 + parent.viewport.y,
                        parent.cursor_x + parent.viewport.x)
                parent.mark_dirty()

            # edit/view note

            # add block
            elif ch == ord("b"):
                if not self.block:
                    self.block = (self.cursor_y + self.map.viewport_y,
                                  self.cursor_x + self.map.viewport_x)
                    self.default_dirty = True
                else:
                    yx2 = ( self.cursor_y + self.map.viewport_y,
                            self.cursor_x + self.map.viewport_x)


                    if self.block[0] == yx2[0] and self.block[1] == yx2[1]:
                        self.map.add_feature(
                                yx2[0]-1,
                                yx2[1],
                                self.current_obj)
                        self.default_dirty = True

                    else:
                        y_max = max([self.block[0], yx2[0]])
                        y_min = min([self.block[0], yx2[0]])

                        x_max = max([self.block[1], yx2[1]])
                        x_min = min([self.block[1], yx2[1]])

                        y_diff = (y_max - y_min) + 1
                        x_diff = (x_max - x_min) + 1


                        for y in range(y_diff):
                            for x in range(x_diff):
                                self.map.add_feature(
                                        y+y_min-1,
                                        x+x_min,
                                        self.current_obj)

                        self.default_screen.move(self.cursor_y, self.cursor_x)
                    self.default_dirty = True
                    self.block = None

            # remove block
            elif ch == ord("X"):
                if not self.x_block:
                    self.x_block = (self.cursor_y + self.map.viewport_y,
                                  self.cursor_x + self.map.viewport_x)
                    self.default_dirty = True
                else:
                    yx2 = ( self.cursor_y + self.map.viewport_y,
                            self.cursor_x + self.map.viewport_x)


                    if self.x_block[0] == yx2[0] and self.x_block[1] == yx2[1]:
                        self.map.add_feature(
                                yx2[0]-1,
                                yx2[1],
                                self.current_obj)
                        self.default_dirty = True

                    else:
                        y_max = max([self.x_block[0], yx2[0]])
                        y_min = min([self.x_block[0], yx2[0]])

                        x_max = max([self.x_block[1], yx2[1]])
                        x_min = min([self.x_block[1], yx2[1]])

                        y_diff = (y_max - y_min) + 1
                        x_diff = (x_max - x_min) + 1


                        for y in range(y_diff):
                            for x in range(x_diff):
                                self.map.rm_feature(
                                        y+y_min-1,
                                        x+x_min)

                        self.default_screen.move(self.cursor_y, self.cursor_x)
                    self.default_dirty = True
                    self.x_block = None

            elif ch == 27: # escape
                if self.block:
                    self.block = None
                    self.default_dirty = True
                if self.x_block:
                    self.x_block = None
                    self.default_dirty = True


            # catch object type
            elif ch == ord("c"):
                self.current_obj = FeatureType.chair
                self.default_dirty = True

            elif ch == ord("d"):
                self.current_obj = FeatureType.door
                self.default_dirty = True

            elif ch == ord("w"):
                self.current_obj = FeatureType.wall
                self.default_dirty = True

            elif ch == ord("t"):
                self.current_obj = FeatureType.table
                self.default_dirty = True

            elif ch == ord(">"):
                self.current_obj = FeatureType.up_stair
                self.default_dirty = True

            elif ch == ord("<"):
                self.current_obj = FeatureType.down_stair
                self.default_dirty = True

            elif ch == ord("%"):
                self.current_obj = FeatureType.lantern
                self.default_dirty = True

            elif ch == ord("#"):
                self.current_obj = FeatureType.chest
                self.default_dirty = True

            elif ch == ord("*"):
                self.current_obj = FeatureType.point_of_interest
                self.default_dirty = True

            elif ch == ord("r"):
                self.current_obj = FeatureType.road
                self.default_dirty = True

            elif ch == ord("G"):
                self.current_obj = FeatureType.gate
                self.default_dirty = True

            elif ch == ord("W"):
                self.current_obj = FeatureType.water
                self.default_dirty = True

            elif ch == ord("T"):
                self.current_obj = FeatureType.tree
                self.default_dirty = True

            elif ch == ord("o"):
                self.current_obj = FeatureType.bush
                self.default_dirty = True

            elif ch == ord("."):
                self.current_obj = FeatureType.grass
                self.default_dirty = True

            elif ch == ord(","):
                self.current_obj = FeatureType.friendly_unit
                self.default_dirty = True

            elif ch == ord("@"):
                self.current_obj = FeatureType.enemy_unit
                self.default_dirty = True

            elif ch == ord("$"):
                self.current_obj = FeatureType.dead_unit
                self.default_dirty = True

            elif ch == ord("^"):
                self.current_obj = FeatureType.hill
                self.default_dirty = True


            # show help
            elif ch == ord("?"):
                self.help()

