import curses
import locale
import colors
import log

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

log = log.logger

types_id = 0
types = []

def new_feature(feature_type, x, y):
    return {
            "y": y,
            "x": x,
            "type": feature_type["name"],
    }

def get_feature_type(name):
    return [ feature for feature in types if feature["name"] == name ][0]


def draw(viewer, screen, feature, x, y, h, w):
    from viewport import Viewport

    if ( feature["x"] >= x and feature["x"] <= x+w and
            feature["y"] >= y and feature["y"] <= y+h ):

        from state import State
        state = viewer.get_submodule(State)
        role = state.get_state("role")

        feature_type = get_feature_type(feature["type"])

        if role == "gm":
            screen.addstr(
                    feature["y"]+1,
                    feature["x"]+1,
                    feature_type["character"],
                    curses.color_pair(feature_type["color_id"])
                    | curses.A_REVERSE)
        elif role == "pc":
            screen.addstr(
                    feature["y"]+1,
                    feature["x"]+1,
                    feature_type["character"],
                    curses.color_pair(feature_type["color_id"]))
        #except:
        #    pass
