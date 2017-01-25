import curses
import locale
import colors
import logging

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

log = logging.getLogger('simple_example')

types_id = 0
types = []

def new_feature(feature_type, x, y):
    return {
            "y": y,
            "x": x,
            "type": feature_type["name"],
            "notes": ""
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
            if feature["notes"] == "":
                screen.addstr(
                        feature["y"],
                        feature["x"],
                        feature_type["character"],
                        curses.color_pair(feature_type["color_id"]))
            else:
                screen.addstr(
                        feature["y"],
                        feature["x"],
                        feature_type["character"],
                        curses.color_pair(feature_type["color_id"])
                        | curses.A_REVERSE)
        elif role == "pc":
            screen.addstr(
                    feature["y"],
                    feature["x"],
                    feature_type["character"],
                    curses.color_pair(feature_type["color_id"]))
        #except:
        #    pass
