from viewer import ViewerConstants
from state import State
from interactive import VisibleModule, FeatureModule, SavableModule, InteractiveModule
from status_line import StatusLine
import colors
import features
import curses
import log
import math

log = log.logger

# TODO: Implement save method

class Viewport(VisibleModule, FeatureModule, SavableModule, InteractiveModule):
    def __init__(self):


        self.initial_draw_priority = 0
        self.draw_priority = 1

        self.x = 0
        self.y = 0
        self.h = 100
        self.w = 100

        self._features = []
        self._units = []
        self._fow = [ [ False for y in range(self.h) ] for x in range(self.w) ]

        self.cursor_y = math.floor(self.h/4)
        self.cursor_x = math.floor(self.w/2)

        self.box_xy = None

        self._screen = curses.newpad(self.h, self.w)
        self._dirty = True

    def draw(self, viewer, force=False):
        if self._dirty or force:
            if force: log.debug("viewport.draw forced")
            if self._dirty: log.debug("viewport is dirty")
            self._screen.erase()

            self._screen.attrset(colors.get("White"))
            self._screen.border(
                    curses.ACS_BOARD,
                    curses.ACS_BOARD,
                    curses.ACS_BOARD,
                    curses.ACS_BOARD,
                    curses.ACS_BOARD,
                    curses.ACS_BOARD,
                    curses.ACS_BOARD,
                    curses.ACS_BOARD
            )
            self._screen.attroff(colors.get("White"))

            [ features.draw(viewer, self._screen, feature, self.x, self.y, self.h, self.w) for feature in self._features ]

            [ unit.draw(viewer, self._screen) for unit in self._units ]


            state = viewer.get_submodule(State)
            if state.get_state("role") == "pc" or (state.get_state("role") == "gm" and state.get_state("fow") == "on"):
                for x in range(0, self.w-2):
                    for y in range(0, self.h-2):
                        if self._fow[x][y]:
                            self._screen.addstr(y+1, x+1, "▒", colors.get("Dark Grey"))

            if self.box_xy != None:
                x_min = min(self.box_xy[0], self.cursor_x)
                x_max = max(self.box_xy[0], self.cursor_x) + 1

                y_min = min(self.box_xy[1], self.cursor_y)
                y_max = max(self.box_xy[1], self.cursor_y) + 1

                for y in range(y_min, y_max):
                    for x in range(x_min, x_max):
                        self._screen.addstr(y, x, "▒", colors.get("Orange"))

            self._screen.addch(self.cursor_y, self.cursor_x, ord('X'), colors.get("Gold"))

            self._screen.noutrefresh(
                    self.y,
                    self.x,
                    0, math.floor(ViewerConstants.max_x/3),
                    ViewerConstants.max_y-3,
                    math.floor(ViewerConstants.max_x/2)+math.floor(ViewerConstants.max_x/3))
            self._dirty = False
            return True
        return False

    def _handle(self, viewer, ch):

        if ch == ord("+") or ch == ord("="):

            unit = self.get_current_unit()
            if unit:
                unit.current_health += 1

                self.client.send({
                    "type": "command",
                    "key": "modify.map.unit",
                    "details": unit.toDict()
                })


        elif ch == ord("-"):
            unit = self.get_current_unit()
            if unit:
                unit.current_health -= 1

                self.client.send({
                    "type": "command",
                    "key": "modify.map.unit",
                    "details": unit.toDict()
                })



    def _handle_help(self, viewer, buf):
        pass

    def _handle_combo(self, viewer, buf):
        pass

    def right(self):
        if self.w - self.x > math.floor(ViewerConstants.max_x/2)+1:
            self.x += 1
            self.cursor_right()
            self._dirty = True

    def down(self):
        if (self.h - self.y) > ViewerConstants.max_y-2:
            self.y += 1
            self.cursor_down()
            self._dirty = True

    def up(self):
        if self.y-1 >= 0:
            self.y -= 1
            self.cursor_up()
            self._dirty = True

    def left(self):
        if self.x-1 >= 0:
            self.x -= 1
            self.cursor_left()
            self._dirty = True

    def cursor_up(self):
        if self.cursor_y-1 >= 1:
            self.cursor_y -= 1
            self._dirty = True

    def cursor_down(self):
        if ( self.cursor_y + 1 < ViewerConstants.max_y-2 + self.y and
             self.cursor_y + 1 < self.h-1 ):
            self.cursor_y +=1
            self._dirty = True

    def cursor_right(self):
        if ( self.cursor_x + 1 < math.floor(ViewerConstants.max_x/2) +1 + self.x and
             self.cursor_x + 1 < self.w-1 ):
            self.cursor_x +=1
            self._dirty = True

    def cursor_left(self):
        if self.cursor_x-1 >= 1:
            self.cursor_x -= 1
            self._dirty = True

    def get_cursor_focus(self, viewer):
        state = viewer.get_submodule(State)
        unit = [ unit for unit in self._units if unit.y == self.cursor_y and unit.x == self.cursor_x ]
        feature = [feature for feature in self._features if feature["y"] == self.cursor_y and feature["x"] == self.cursor_x]

        if not (state.get_state("role") == "pc" and self._fow[self.cursor_x][self.cursor_y]):
        # ensures there is a feature and if we are a pc we will not show thing hidden by FoW
            if len(unit):
                sl = viewer.get_submodule(StatusLine)
                                #name + space         border []
                text = "%s %s/%s " % (unit[0].name, unit[0].current_health, unit[0].max_health)
                bar = ""

                if unit[0].max_health != 0:
                    width = sl.w - (len(text) + 1) - 2 - 2

                    percent = unit[0].current_health/float(unit[0].max_health)

                    if percent <= 1.0 and percent >= 0.0:
                        number_of_units = math.ceil(percent * width)
                        bar = number_of_units * "="
                        bar = bar.rjust(width, " ")

                    elif percent > 1.0:
                        diff = percent - 1.0
                        diff_percent = diff/percent
                        excess = math.ceil(width * diff_percent)

                        bar = excess * "="
                        bar += "(+)|"
                        bar = bar.ljust(width, "=")

                    elif percent < 0.0:
                        diff = (-1 * percent)/(1.0 + ( -1 * percent))
                        log.error("diff %s" % diff)
                        excess = math.ceil(width * diff)

                        bar = "|(-)"
                        bar += excess * "="
                        bar = bar.rjust(width, " ")


                desc = "%s [%s]" % (text, bar)
                return desc

            elif(len(feature)):
                desc = "%s" % feature[0]["type"]
                return desc

        return ""


    def get_feature_idx(self, y, x):
        for feature in self._features:
            if feature["y"] == y and feature["x"] == x:
                return self._features.index(feature)

    def get_feature(self, idx):
        return self._features[idx]

    def update_feature(self, idx, feature):
        self._features[idx] = feature

    def serialize_features(self):
        features = []
        for feature in self._features:
            features.append(feature)
        return features

    def update_features(self, feature_dicts):
        self._features = []
        for feature_dict in feature_dicts:
            self._features.append(feature_dict)

        if len(feature_dicts):
            self._dirty = True

    def set_fow(self, new_fow):
        self._fow = new_fow
        self._dirty = True

    def add_fow(self, point):
        self._fow[point["x"]][point["y"]] = True
        self._dirty = True

    def remove_fow(self, point):
        log.info(("point", point))
        self._fow[point["x"]][point["y"]] = False
        self._dirty = True

    def update_units(self, units):
        self._units = units
        self._dirty = True

    def update_screen(self, max_y, max_x):
        self.h = max_y + 1
        self.w = max_x + 2

        del self._screen
        self._screen = curses.newpad(self.h, self.w)

    def get_current_unit(self):
        for unit in self._units:
            if unit.y == self.cursor_y and unit.x == self.cursor_x:
                return unit
        return None

