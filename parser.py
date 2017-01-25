import colors
import keybindings
import features
import math
import curses


def add_color(name, r, g, b):
    id = colors.color_id
    colors.colors.append({
        "id": id,
        "name": name,
        "r": scale_color(r),
        "g": scale_color(g),
        "b": scale_color(b)
    })
    colors.color_id += 1

    colors.color_pairs.append({
        "id": colors.color_pair_id,
        "name": name,
        "fore": id,
        "back": 0
        })
    colors.color_pair_id += 1

def add_color_pair(name, fore, back):

    fore_id = None
    back_id = None

    for color in colors.colors:
        if color["name"] == fore:
            fore_id = color["id"]
        if color["name"] == back:
            back_id = color["id"]

    if (fore_id is not None and
            back_id is not None):

        colors.color_pairs.append({
            "id": colors.color_pair_id,
            "name": name,
            "fore": fore_id,
            "back": back_id
            })
        colors.color_pair_id += 1

def scale_color(color):
    return math.ceil((color/255)*1000)

def add_feature(name, character, color):
    features.types.append({
        "name": name,
        "character": character,
        "color_name": color
    })

def add_build_menu_keybind(feature_name, key):
    for feature in features.types:
        if feature["name"] == feature_name:
            keybindings.build.append({
                "type": feature["name"],
                "key": key
            })


def load_config():

    # init colors
    curses.start_color()
    if curses.can_change_color():
        curses.init_color(0, 0, 0, 0)
        curses.init_color(1, 0, 0, 0)
        curses.init_color(2, 255, 255, 255)

        for color in colors.colors:
            curses.init_color(
                color["id"],
                color["r"],
                color["g"],
                color["b"])


    for cp in colors.color_pairs:

        curses.init_pair(
            cp["id"],
            cp["fore"],
            cp["back"])

    for feature in features.types:
        for cp in colors.color_pairs:
            if cp["name"] == feature["color_name"]:
                feature["color_id"] = cp["id"]

    for binding in keybindings.build:
        for feature in features.types:
            if binding["type"] == feature["name"]:
                binding["type"] = feature



add_color("Black", 0, 0, 0)
add_color("White", 255, 255, 255)
add_color_pair("White", "White", "Black")
