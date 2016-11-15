import curses

class Editor:

    def __init__(self, screen, map, save_handler, min_y=None, min_x=None, max_y=None, max_x=None):
        self.min_y = min_y if min_y else 0
        self.min_x = min_x if min_x else  0
        self.max_y = max_y if max_y else (curses.LINES - 1)
        self.max_x = max_x if max_x else (curses.COLS - 1)

        self.cursor_y = int(self.max_y/2)
        self.cursor_x = int(self.max_x/2)

        self.default_cursor_y = int(self.max_y/2)
        self.default_cursor_x = int(self.max_x/2)

        self.map = map

        self.save_handler = save_handler

        self.default_screen = screen
        #self.default_screen.clear()

        self.exit = False
        self.colon = False
        self.comon_char = None

        self.current_obj = FeatureType.wall

        self.default_dirty = True

    def draw(self):
        if self.default_dirty:
            #self.default_screen.clear()
            self.set_status_line("CUR(%s, %s), VP(%s, %s), MODE(%s)" % (self.cursor_y, self.cursor_x, self.map.viewport_y, self.map.viewport_x, FeatureType.toName(self.current_obj)))
            self.map.draw(force=True)
            self.default_screen.move(self.cursor_y, self.cursor_x)
            self.default_screen.noutrefresh()
            self.default_dirty = False

        else:
            self.map.draw()
        curses.doupdate()

    def set_status_line(self, msg):
        padded = msg.ljust(self.max_x)
        self.default_screen.addstr(0,0, padded)


    def handle(self, ch):

        if self.colon:
            if ch == ord("w"):
                self.default_screen.addstr(self.max_y,0, "Colon Mode: w")
                self.colon = True
                self.colon_char = "w"

            if ch == ord("q"):
                self.default_screen.addstr(self.max_y,0, "Colon Mode: q")
                self.colon = True
                self.colon_char = "q"

            if ch == 27:
                self.colon = False
                self.colon_char = None
                self.default_dirty = True

            if ch == curses.KEY_ENTER or ch == 10 or ch == 13:
                if self.colon_char == "w":
                    json_map = self.map.serialize()
                    self.save_handler(json_map)
                    self.default_dirty = True

                if self.colon_char == "q":
                    exit()

                self.colon = False
                self.colon_char = None

        else:
            if ch == ord(":"):
                self.colon = True
                self.default_screen.addstr(self.max_y,0, "Colon Mode: ")

            # quit
            if ch == ord("z"):
                if not self.exit:
                    self.exit = True
                elif self.exit:
                    exit()
            elif self.exit:
                self.exit = False


            # detect movement
            if ch == ord("j"):
                if self.cursor_y + 1 <= self.max_y-1:
                    self.cursor_y += 1
                    self.default_screen.move(self.cursor_y, self.cursor_x)
                    self.default_dirty = True

            if ch == ord("J"):
                self.map.move_viewport_pos_y()
                self.default_screen.move(self.default_cursor_y, self.default_cursor_x)
                self.default_dirty = True

            if ch == ord("k"):
                if self.cursor_y - 1 >= self.min_y+2:
                    self.cursor_y -= 1
                    self.default_screen.move(self.cursor_y, self.cursor_x)
                    self.default_dirty = True

            if ch == ord("K"):
                self.map.move_viewport_neg_y()
                self.default_screen.move(self.default_cursor_y, self.default_cursor_x)
                self.default_dirty = True

            if ch == ord("h"):
                if self.cursor_x - 1 >= self.min_x+1:
                    self.cursor_x -= 1
                    self.default_screen.move(self.cursor_y, self.cursor_x)
                    self.default_dirty = True

            if ch == ord("H"):
                self.map.move_viewport_neg_x()
                self.default_screen.move(self.default_cursor_y, self.default_cursor_x)
                self.default_dirty = True

            if ch == ord("l"):
                if self.cursor_x + 1 <= self.max_x-1:
                    self.cursor_x += 1
                    self.default_screen.move(self.cursor_y, self.cursor_x)
                    self.default_dirty = True

            if ch == ord("L"):
                self.map.move_viewport_pos_x()
                self.default_screen.move(self.default_cursor_y, self.default_cursor_x)
                self.default_dirty = True

            # detect place object
            if ch == ord(" "):
                self.map.add_feature(self.cursor_y-1, self.cursor_x, self.current_obj)
                self.default_dirty = True

            if ch == ord("x"):
                self.map.rm_feature(self.cursor_y-1, self.cursor_x)
                self.default_dirty = True

            if ch == ord("c"):
                self.current_obj = FeatureType.chair
                self.default_dirty = True

            if ch == ord("d"):
                self.current_obj = FeatureType.door
                self.default_dirty = True

            if ch == ord("w"):
                self.current_obj = FeatureType.wall
                self.default_dirty = True

            if ch == ord("t"):
                self.current_obj = FeatureType.table
                self.default_dirty = True

            if ch == ord(">"):
                self.current_obj = FeatureType.up_stair
                self.default_dirty = True

            if ch == ord("<"):
                self.current_obj = FeatureType.down_stair
                self.default_dirty = True

            if ch == ord("%"):
                self.current_obj = FeatureType.lantern
                self.default_dirty = True

            if ch == ord("#"):
                self.current_obj = FeatureType.chest
                self.default_dirty = True

            if ch == ord("*"):
                self.current_obj = FeatureType.point_of_interest
                self.default_dirty = True

            if ch == ord("r"):
                self.current_obj = FeatureType.road
                self.default_dirty = True

            if ch == ord("G"):
                self.current_obj = FeatureType.gate
                self.default_dirty = True

            if ch == ord("W"):
                self.current_obj = FeatureType.water
                self.default_dirty = True


        # detect screen resize
        #if curses.KEY_RESIZE:
        #    self.max_y = (curses.LINES - 1)
        #    self.max_x = (curses.COLS - 1)

        #    self.default_screen.clear()
        #    self.default_screen.border("|", "|", "-", "-", "+", "+", "+", "+")
        #    self.default_dirty = True

def init():
    FeatureType.init()

class FeatureType:
    def init():
        FeatureType.wall = curses.ACS_BOARD
        FeatureType.table = ord("t")
        FeatureType.chair = ord("c")
        FeatureType.door = ord("D")
        FeatureType.up_stair = curses.ACS_UARROW
        FeatureType.down_stair = curses.ACS_DARROW
        FeatureType.lantern = ord("%")
        FeatureType.road = curses.ACS_BOARD
        FeatureType.chest = ord("#")
        FeatureType.point_of_interest = ord("*")
        FeatureType.gate = ord("G")
        FeatureType.water = ord("~")

    def toName(char):
        if char == FeatureType.wall:
            return "Wall"
        elif char == FeatureType.table:
            return "Table"
        elif char == FeatureType.chair:
            return "Chair"
        elif char == FeatureType.up_stair:
            return "Up Stair"
        elif char == FeatureType.down_stair:
            return "Down Stair"
        elif char == FeatureType.door:
            return "Door"
        elif char == FeatureType.lantern:
            return "Lantern"
        elif char == FeatureType.chest:
            return "Chest"
        elif char == FeatureType.point_of_interest:
            return "Point of Interest"
        elif char == FeatureType.road:
            return "Road"
        elif char == FeatureType.gate:
            return "Gate"
        elif char == FeatureType.water:
            return "Water"

    def fromName(name):
        if name == "Wall":
            return FeatureType.wall
        elif name == "Table":
            return FeatureType.table
        elif name == "Chair":
            return FeatureType.chair
        elif name == "Up Stair":
            return FeatureType.up_stair
        elif name == "Down Stair":
            return FeatureType.down_stair
        elif name == "Door":
            return FeatureType.door
        elif name == "Lantern":
            return FeatureType.lantern
        elif name == "Chest":
            return FeatureType.chest
        elif name == "Point of Interest":
            return FeatureType.point_of_interest
        elif name == "Road":
            return FeatureType.road
        elif name == "Gate":
            return FeatureType.gate
        elif name == "Water":
            return FeatureType.water

    def modFromName(name):
        if name == "Wall":
            return None
        elif name == "Table":
            return None
        elif name == "Chair":
            return None
        elif name == "Up Stair":
            return None
        elif name == "Down Stair":
            return None
        elif name == "Door":
            return None
        elif name == "Lantern":
            return None
        elif name == "Chest":
            return None
        elif name == "Point of Interest":
            return None
        elif name == "Road":
            return curses.color_pair(1)
        elif name == "Gate":
            return None
        elif name == "Water":
            return curses.color_pair(5)


class FeatureSerializer:
    def toDict(obj):
        return {
                "y": obj.pos_y,
                "x": obj.pos_x,
                "type": FeatureType.toName(obj.char)
        }

    def fromDict(obj):
        return Feature(
                obj["y"],
                obj["x"],
                FeatureType.fromName(
                    obj["type"]
                ),
                mod=FeatureType.modFromName(
                    obj["type"]
                ))


class Feature:
    def __init__(self, pos_y, pos_x, char, mod=None):
        self.pos_y = pos_y
        self.pos_x = pos_x
        self.char=char
        self.mod = mod

    def draw(self, screen):
        if self.mod:
            screen.addch(
                    self.pos_y,
                    self.pos_x,
                    self.char,
                    self.mod)
        else:
            screen.addch(
                    self.pos_y,
                    self.pos_x,
                    self.char)


class Rectangle(Feature):
    def __init__(self, pos_y, pos_x, w, h, char):
        shape = [ char for x in range(h) for y in range(w) ]
        super(Feature).__init__(pos_y, pos_x, shape)



class Map:

    def __init__(self, map_obj, screen_max_x=None, screen_max_y=None):
        self.map_obj = map_obj
        self.features = []

        for feature in map_obj["features"]:
            self.features.append(
                FeatureSerializer.fromDict(feature)
            )

        self.max_y = self.map_obj["max_y"]
        self.max_x = self.map_obj["max_x"]

        self.screen_max_x = screen_max_x if screen_max_x else curses.COLS-1
        self.screen_max_y = screen_max_y if screen_max_y else curses.LINES-1

        self.viewport_x = 0
        self.viewport_y = 0
        self.viewport_h = self.screen_max_y
        self.viewport_w = self.screen_max_x

        self.pad = curses.newpad(self.max_y+2, self.max_x+2)
        self.dirty = True




    def draw(self, force=False):
        if self.dirty or force:

            self.pad.clear()
            self.pad.border(
                    curses.ACS_BOARD,
                    curses.ACS_BOARD,
                    curses.ACS_BOARD,
                    curses.ACS_BOARD,
                    curses.ACS_BOARD,
                    curses.ACS_BOARD,
                    curses.ACS_BOARD,
                    curses.ACS_BOARD
            )

            for feature in self.features:
                feature.draw(self.pad)

            self.pad.noutrefresh(
                    self.viewport_y,
                    self.viewport_x,
                    1,0,
                    self.viewport_h, self.viewport_w)
            self.dirty = False


    def add_feature(feature):
        self.map_obj["features"].append(feature)
        self.dirty = True

    def move_viewport_pos_x(self):
        if self.max_x - self.viewport_x > self.screen_max_x-1:
            self.viewport_x += 1
            self.dirty = True

    def move_viewport_pos_y(self):
        if (self.max_y - self.viewport_y) > self.screen_max_y-2:
            self.viewport_y += 1
            self.dirty = True

    def move_viewport_neg_y(self):
        if self.viewport_y-1 >= 0:
            self.viewport_y -= 1
            self.dirty = True

    def move_viewport_neg_x(self):
        if self.viewport_x-1 >= 0:
            self.viewport_x -= 1
            self.dirty = True

    def add_feature(self, y, x, char):
        self.features.append(
            Feature(y, x, char, mod=FeatureType.modFromName(
                                    FeatureType.toName(char)
                                ))
        )
        self.dirty = True

    def rm_feature(self, y, x):
        for feature in self.features:
            if feature.pos_y is y and feature.pos_x is x:
                self.features.remove(feature)
                break

    def serialize(self):
        features = []
        for feature in self.features:
            features.append(FeatureSerializer.toDict(feature))
        self.map_obj["features"] = features
        return self.map_obj






