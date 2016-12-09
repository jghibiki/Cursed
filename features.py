import curses
import locale
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

def init_features():
    FeatureType.init()

def load_features(map_obj):
    features = []
    for feature in map_obj["features"]:
        features.append(
            FeatureSerializer.fromDict(feature))
    return features

class FeatureType:
    def init():
        FeatureType.wall = 0
        FeatureType.table = 1
        FeatureType.chair = 2
        FeatureType.door = 3
        FeatureType.up_stair = 4
        FeatureType.down_stair = 5
        FeatureType.lantern = 6
        FeatureType.road = 7
        FeatureType.chest = 8
        FeatureType.point_of_interest = 9
        FeatureType.gate = 10
        FeatureType.water = 11
        FeatureType.tree = 12
        FeatureType.bush = 13
        FeatureType.grass = 14
        FeatureType.friendly_unit = 15
        FeatureType.enemy_unit = 16
        FeatureType.dead_unit = 17
        FeatureType.hill = 18
        FeatureType.bed = 19
        FeatureType.statue = 20

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
        elif char == FeatureType.tree:
            return "Tree"
        elif char == FeatureType.bush:
            return "Bush"
        elif char == FeatureType.grass:
            return "Grass"
        elif char == FeatureType.friendly_unit:
            return "Friendly Unit"
        elif char == FeatureType.enemy_unit:
            return "Enemy Unit"
        elif char == FeatureType.dead_unit:
            return "Dead Unit"
        elif char == FeatureType.hill:
            return "Hill"
        elif char == FeatureType.bed:
            return "Bed"
        elif char == FeatureType.statue:
            return "Statue"

    def toSymbol(id):
        if id == FeatureType.wall:
            return "▒"
        elif id == FeatureType.table:
            return "T"
        elif id == FeatureType.chair:
            return "c"
        elif id == FeatureType.door:
            return "D"
        elif id == FeatureType.up_stair:
            return "↑"
        elif id == FeatureType.down_stair:
            return "↓"
        elif id == FeatureType.lantern:
            return "%"
        elif id == FeatureType.road:
            return "▒"
        elif id == FeatureType.chest:
            return "#"
        elif id == FeatureType.point_of_interest:
            return "*"
        elif id == FeatureType.gate:
            return "G"
        elif id == FeatureType.water:
            return "~"
        elif id == FeatureType.tree:
            return "O"
        elif id == FeatureType.bush:
            return "o"
        elif id == FeatureType.grass:
            return "."
        elif id == FeatureType.friendly_unit:
            return "@"
        elif id == FeatureType.enemy_unit:
            return "@"
        elif id == FeatureType.dead_unit:
            return "@"
        elif id == FeatureType.hill:
            return "^"
        elif id == FeatureType.bed:
            return "b"
        elif id == FeatureType.statue:
            return "&"
        else:
            return u"\u2699".encode(code)

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
        elif name == "Tree":
            return FeatureType.tree
        elif name == "Bush":
            return FeatureType.bush
        elif name == "Grass":
            return FeatureType.grass
        elif name == "Friendly Unit":
            return FeatureType.friendly_unit
        elif name == "Enemy Unit":
            return FeatureType.enemy_unit
        elif name == "Dead Unit":
            return FeatureType.dead_unit
        elif name == "Hill":
            return FeatureType.hill
        elif name == "Bed":
            return FeatureType.bed
        elif name == "Statue":
            return FeatureType.statue

    def modFromName(name):
        if name == "Wall":
            return curses.color_pair(95)
        elif name == "Table":
            return curses.A_NORMAL
        elif name == "Chair":
            return curses.A_NORMAL
        elif name == "Up Stair":
            return curses.A_NORMAL
        elif name == "Down Stair":
            return curses.A_NORMAL
        elif name == "Door":
            return curses.color_pair(95)
        elif name == "Lantern":
            return curses.color_pair(4)
        elif name == "Chest":
            return curses.A_NORMAL
        elif name == "Point of Interest":
            return curses.color_pair(197)
        elif name == "Road":
            return curses.color_pair(12)
        elif name == "Gate":
            return curses.color_pair(95)
        elif name == "Water":
            return curses.color_pair(5)
        elif name == "Tree":
            return curses.color_pair(95)
        elif name == "Bush":
            return curses.color_pair(29)
        elif name == "Grass":
            return curses.color_pair(29)
        elif name == "Friendly Unit":
            return curses.color_pair(47)
        elif name == "Enemy Unit":
            return curses.color_pair(197)
        elif name == "Dead Unit":
            return curses.color_pair(8)
        elif name == "Hill":
            return curses.A_NORMAL
        elif name == "Bed":
            return curses.A_NORMAL
        elif name == "Statue":
            return curses.A_NORMAL


class FeatureSerializer:
    def toDict(obj):
        return {
                "y": obj.pos_y,
                "x": obj.pos_x,
                "type": FeatureType.toName(obj.char),
                "notes": obj.notes
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
                ),
                notes=obj["notes"])


class Feature:
    def __init__(self, pos_y, pos_x, char, mod=None, notes=""):
        self.pos_y = pos_y
        self.pos_x = pos_x
        self.char = char
        self.mod = mod
        self.notes = notes

    def draw(self, viewer, screen):
        from state import State
        state = viewer.get_submodule(State)
        role = state.get_state("role")
        try:
            if role == "gm":
                if self.mod and self.notes == "":
                    screen.addstr(
                            self.pos_y,
                            self.pos_x,
                            FeatureType.toSymbol(self.char),
                            self.mod)
                elif self.mod and self.notes != "":
                    screen.addstr(
                            self.pos_y,
                            self.pos_x,
                            FeatureType.toSymbol(self.char),
                            self.mod |
                            curses.A_BLINK)
                elif not self.mod and self.notes != "" :
                    screen.addstr(
                            self.pos_y,
                            self.pos_x,
                            FeatureType.toSymbol(self.char),
                            curses.A_BLINK)
                elif not self.mod and self.notes == "":
                    screen.addstr(
                        self.pos_y,
                        self.pos_x,
                        FeatureType.toSymbol(self.char))
            elif role == "pc":
                if self.mod:
                    screen.addstr(
                            self.pos_y,
                            self.pos_x,
                            FeatureType.toSymbol(self.char),
                            self.mod)
                elif not self.mod:
                    screen.addstr(
                        self.pos_y,
                        self.pos_x,
                        FeatureType.toSymbol(self.char))
        except:
            pass


