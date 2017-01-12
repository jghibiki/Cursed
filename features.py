import curses
import locale
from colors import Colors
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
        FeatureType.blood = 21
        FeatureType.fire = 22
        FeatureType.snow = 23
        FeatureType.boulder = 24

    def toName(character):
        if character == FeatureType.wall:
            return "Wall"
        elif character == FeatureType.table:
            return "Table"
        elif character == FeatureType.chair:
            return "Chair"
        elif character == FeatureType.up_stair:
            return "Up Stair"
        elif character == FeatureType.down_stair:
            return "Down Stair"
        elif character == FeatureType.door:
            return "Door"
        elif character == FeatureType.lantern:
            return "Lantern"
        elif character == FeatureType.chest:
            return "Chest"
        elif character == FeatureType.point_of_interest:
            return "Point of Interest"
        elif character == FeatureType.road:
            return "Road"
        elif character == FeatureType.gate:
            return "Gate"
        elif character == FeatureType.water:
            return "Water"
        elif character == FeatureType.tree:
            return "Tree"
        elif character == FeatureType.bush:
            return "Bush"
        elif character == FeatureType.grass:
            return "Grass"
        elif character == FeatureType.friendly_unit:
            return "Friendly Unit"
        elif character == FeatureType.enemy_unit:
            return "Enemy Unit"
        elif character == FeatureType.dead_unit:
            return "Dead Unit"
        elif character == FeatureType.hill:
            return "Hill"
        elif character == FeatureType.bed:
            return "Bed"
        elif character == FeatureType.statue:
            return "Statue"
        elif character == FeatureType.blood:
            return "Blood"
        elif character == FeatureType.fire:
            return "Fire"
        elif character == FeatureType.snow:
            return "Snow"
        elif character == FeatureType.boulder:
            return "Boulder"

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
        elif id == FeatureType.blood:
            return "▒"
        elif id == FeatureType.fire:
            return "~"
        elif id == FeatureType.snow:
            return "▒"
        elif id == FeatureType.boulder:
            return "O"
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
        elif name == "Blood":
            return FeatureType.blood
        elif name == "Fire":
            return FeatureType.fire
        elif name == "Snow":
            return FeatureType.snow
        elif name == "Boulder":
            return FeatureType.boulder

    def modFromName(name):
        if name == "Wall":
            return Colors.get(Colors.BROWN)
        elif name == "Table":
            return curses.A_NORMAL
        elif name == "Chair":
            return curses.A_NORMAL
        elif name == "Up Stair":
            return curses.A_NORMAL
        elif name == "Down Stair":
            return curses.A_NORMAL
        elif name == "Door":
            return Colors.get(Colors.BROWN)
        elif name == "Lantern":
            return Colors.get(Colors.GOLD)
        elif name == "Chest":
            return curses.A_NORMAL
        elif name == "Point of Interest":
            return Colors.get(Colors.RED)
        elif name == "Road":
            return Colors.get(Colors.GREY)
        elif name == "Gate":
            return Colors.get(Colors.BROWN)
        elif name == "Water":
            return Colors.get(Colors.LIGHT_BLUE)
        elif name == "Tree":
            return Colors.get(Colors.BROWN)
        elif name == "Bush":
            return Colors.get(Colors.DARK_GREEN)
        elif name == "Grass":
            return Colors.get(Colors.GREEN)
        elif name == "Hill":
            return curses.A_NORMAL
        elif name == "Bed":
            return curses.A_NORMAL
        elif name == "Statue":
            return curses.A_NORMAL
        elif name == "Blood":
            return Colors.get(Colors.DARK_RED)
        elif name == "Fire":
            return Colors.get(Colors.RED_ON_ORANGE)
        elif name == "Snow":
            return Colors.get(Colors.WHITE)
        elif name == "Boulder":
            return Colors.get(Colors.DARK_GREY)


class FeatureSerializer:
    def toDict(obj):
        return {
                "y": obj.pos_y,
                "x": obj.pos_x,
                "type": FeatureType.toName(obj.character),
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
    def __init__(self, pos_y, pos_x, character, mod=None, notes=""):
        self.pos_y = pos_y
        self.pos_x = pos_x
        self.character = character
        self.mod = mod
        self.symbol = FeatureType.toSymbol(self.character)
        self.notes = notes
        self.state = None

    def draw(self, viewer, screen, x, y, h, w):
        if ( self.pos_x >= x and self.pos_x <= x+w and
                self.pos_y >= y and self.pos_y <= y+h ):
            if self.state is None:
                from state import State
                self.state = viewer.get_submodule(State)
            role = self.state.get_state("role")
            try:
                if role == "gm":
                    if self.mod and self.notes == "":
                        screen.addstr(
                                self.pos_y,
                                self.pos_x,
                                self.symbol,
                                self.mod)
                    elif self.mod and self.notes != "":
                        screen.addstr(
                                self.pos_y,
                                self.pos_x,
                                self.symbol,
                                self.mod |
                                curses.A_REVERSE)
                    elif not self.mod and self.notes != "" :
                        screen.addstr(
                                self.pos_y,
                                self.pos_x,
                                self.symbol,
                                curses.A_BLINK)
                    elif not self.mod and self.notes == "":
                        screen.addstr(
                            self.pos_y,
                            self.pos_x,
                            self.symbol)
                elif role == "pc":
                    if self.mod:
                        screen.addstr(
                                self.pos_y,
                                self.pos_x,
                                self.symbol,
                                self.mod)
                    elif not self.mod:
                        screen.addstr(
                            self.pos_y,
                            self.pos_x,
                            self.symbol)
            except:
                pass


