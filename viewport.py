from features import Feature, FeatureType, FeatureSerializer
from viewer import ViewerConstants
from interactive import VisibleModule, FeatureModule, SavableModule
import curses
import logging

log = logging.getLogger('simple_example')

# TODO: Implement save method

class Viewport(VisibleModule, FeatureModule, SavableModule):
    def __init__(self, features, max_y, max_x):

        self._features = features

        self.draw_priority =1

        self.x = 0
        self.y = 0
        self.h = max_y + 1
        self.w = max_x + 2

        self._screen = curses.newpad(self.h, self.w)
        self._dirty = True

    def draw(self, viewer):
        if self._dirty:
            self._screen.clear()
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

            for feature in self._features:
                feature.draw(self._screen)

            self._screen.noutrefresh(
                    self.y,
                    self.x,
                    1,0,
                    ViewerConstants.max_y,
                    ViewerConstants.max_x)
            return True
        return False

    def move_vp_right(self):
        if self.w - self.x > ViewerConstants.max_x-1:
            self.x += 1
            self.dirty = True

    def move_vp_down(self):
        if (self.h - self.y) > ViewerConstants.max_y-2:
            self.y += 1
            self.dirty = True

    def move_vp_up(self):
        if self.y-1 >= 0:
            self.y -= 1
            self.dirty = True

    def move_vp_left(self):
        if self.x-1 >= 0:
            self.x -= 1
            self.dirty = True

    def add_feature(self, y, x, char):
        if x < self.w and y < self.h:
            # if there is already a feature here don't add another
            for feature in self.features:
                if feature.pos_y == y and feature.pos_x == x:
                    return

            self._features.append(
                Feature(y, x, char,
                    mod=FeatureType.modFromName(
                        FeatureType.toName(char))))
            self.dirty = True

    def rm_feature(self, y, x):
        for feature in self._features:
            if feature.pos_y is y and feature.pos_x is x:
                self.features.remove(feature)
                self.dirty = True
                break

    def get_feature_idx(self, y, x):
        for feature in self._features:
            if feature.pos_y == y and feature.pos_x == x:
                return self._features.index(feature)

    def get_feature(self, idx):
        return self._features[idx]

    def update_feature(self, idx, feature):
        self._features[idx] = feature

    def serialize_features(self):
        features = []
        for feature in self._features:
            features.append(FeatureSerializer.toDict(feature))
        return features

    def update_features(self, feature_dicts):
        self._features = []
        for feature_dict in feature_dicts:
            self._features.append(
                    FeatureSerializer.fromDict(
                        feature_dict))

    def update_screen(self, max_y, max_x):
        self.h = max_y + 1
        self.w = max_x + 2

        del self._screen
        self._screen = curses.newpad(self.h, self.w)
