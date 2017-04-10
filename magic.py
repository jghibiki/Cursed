import subscriptions
import broadcast_server

import json

gm_password = "1111"
password = "2222"

handlers = None
users = []
save = None

game_data = {}
# add at least the staging map
game_data["maps"] = {}
game_data["maps"]["__staging__"] = {
    "max_x": 100,
    "max_y": 100,
    "feature_types": [
        { "name": "Wall",       "character": "\u2588",  "color": "Brown",       "key": "w" },
        { "name": "Table",      "character": "T",       "color": "Brown",       "key": "T" },
        { "name": "Chair",      "character": "c",       "color": "Brown",       "key": "c" },
        { "name": "Door",       "character": "d",       "color": "Brown",       "key": "d" },
        { "name": "Up Stair",   "character": "\u2191",  "color": "Brown",       "key":">" },
        { "name": "Down Stair", "character": "\u2193",  "color": "Brown",       "key": "<" },
        { "name": "Lantern",    "character": "%",       "color": "Gold",        "key": "%" },
        { "name": "Road",       "character": "\u2588",  "color": "Grey",        "key": "r" },
        { "name": "Chest",      "character": "#",       "color": "White",       "key": "#" },
        { "name": "Gate",       "character": "G",       "color": "Brown",       "key": "G" },
        { "name": "Water",      "character": "~",       "color": "Light Blue",  "key": "~" },
        { "name": "Tree",       "character": "O",       "color": "Brown",       "key": "t" },
        { "name": "Bush",       "character": "o",       "color": "Dark Green",  "key":"o" },
        { "name": "Grass",      "character": ".",       "color": "Dark Green",  "key": "." },
        { "name": "Hill",       "character": "^",       "color": "White",       "key": "^" },
        { "name": "Bed",        "character": "b",       "color": "Brown",       "key": "b" },
        { "name": "Statue",     "character": "&",       "color": "White",       "key":"&" },
        { "name": "Blood",      "character": "\u2588",  "color": "Dark Red",    "key":"B" },
        { "name": "Fire",       "character": "~",       "color": "Orange",      "key": "f"},
        { "name": "Snow",       "character": "\u2588",  "color": "White",       "key":"s" },
        { "name": "Boulder",    "character": "O",       "color": "Dark Grey",   "key": "O"}
    ],
    "features": [{"y": 4,"x": 8,"type": "Snow","notes": ""},
        {"y": 4,"x": 7,"type": "Snow","notes": ""},{"y": 4,"x": 6,"type": "Snow","notes": ""},
        {"y": 4,"x": 5,"type": "Snow","notes": ""},{"y": 5,"x": 5,"type": "Snow","notes": ""},
        {"y": 6,"x": 5,"type": "Snow","notes": ""},{"y": 6,"x": 6,"type": "Snow","notes": ""},
        {"y": 6,"x": 7,"type": "Snow","notes": ""},{"y": 6,"x": 8,"type": "Snow","notes": ""},
        {"y": 7,"x": 8,"type": "Snow","notes": ""},{"y": 8,"x": 8,"type": "Snow","notes": ""},
        {"y": 8,"x": 7,"type": "Snow","notes": ""},{"y": 8,"x": 6,"type": "Snow","notes": ""},
        {"y": 8,"x": 5,"type": "Snow","notes": ""},{"y": 6,"x": 10,"type": "Snow","notes": ""},
        {"y": 6,"x": 11,"type": "Snow","notes": ""},{"y": 6,"x": 12,"type": "Snow","notes": ""},
        {"y": 6,"x": 13,"type": "Snow","notes": ""},{"y": 6,"x": 14,"type": "Snow","notes": ""},
        {"y": 4,"x": 12,"type": "Snow","notes": ""},{"y": 5,"x": 12,"type": "Snow","notes": ""},
        {"y": 7,"x": 12,"type": "Snow","notes": ""},{"y": 8,"x": 12,"type": "Snow","notes": ""},
        {"y": 6,"x": 19,"type": "Snow","notes": ""},{"y": 6,"x": 18,"type": "Snow","notes": ""},
        {"y": 6,"x": 17,"type": "Snow","notes": ""},{"y": 6,"x": 16,"type": "Snow","notes": ""},
        {"y": 7,"x": 16,"type": "Snow","notes": ""},{"y": 8,"x": 16,"type": "Snow","notes": ""},
        {"y": 8,"x": 17,"type": "Snow","notes": ""},{"y": 8,"x": 18,"type": "Snow","notes": ""},
        {"y": 8,"x": 19,"type": "Snow","notes": ""},{"y": 7,"x": 19,"type": "Snow","notes": ""},
        {"y": 7,"x": 20,"type": "Snow","notes": ""},{"y": 8,"x": 21,"type": "Snow","notes": ""},
        {"y": 6,"x": 23,"type": "Snow","notes": ""},{"y": 7,"x": 23,"type": "Snow","notes": ""},
        {"y": 8,"x": 23,"type": "Snow","notes": ""},{"y": 8,"x": 24,"type": "Snow","notes": ""},
        {"y": 8,"x": 25,"type": "Snow","notes": ""},{"y": 8,"x": 26,"type": "Snow","notes": ""},
        {"y": 7,"x": 26,"type": "Snow","notes": ""},{"y": 6,"x": 26,"type": "Snow","notes": ""},
        {"y": 6,"x": 25,"type": "Snow","notes": ""},{"y": 6,"x": 24,"type": "Snow","notes": ""},
        {"y": 9,"x": 26,"type": "Snow","notes": ""},{"y": 10,"x": 26,"type": "Snow","notes": ""},
        {"y": 10,"x": 25,"type": "Snow","notes": ""},{"y": 10,"x": 24,"type": "Snow","notes": ""},
        {"y": 10,"x": 23,"type": "Snow","notes": ""},{"y": 6,"x": 28,"type": "Snow","notes": ""},
        {"y": 7,"x": 28,"type": "Snow","notes": ""},{"y": 8,"x": 28,"type": "Snow","notes": ""},
        {"y": 4,"x": 28,"type": "Snow","notes": ""},{"y": 6,"x": 30,"type": "Snow","notes": ""},
        {"y": 7,"x": 30,"type": "Snow","notes": ""},{"y": 8,"x": 30,"type": "Snow","notes": ""},
        {"y": 6,"x": 31,"type": "Snow","notes": ""},{"y": 6,"x": 32,"type": "Snow","notes": ""},
        {"y": 6,"x": 33,"type": "Snow","notes": ""},{"y": 7,"x": 33,"type": "Snow","notes": ""},
        {"y": 8,"x": 33,"type": "Snow","notes": ""},{"y": 6,"x": 35,"type": "Snow","notes": ""},
        {"y": 7,"x": 35,"type": "Snow","notes": ""},{"y": 8,"x": 35,"type": "Snow","notes": ""},
        {"y": 8,"x": 36,"type": "Snow","notes": ""},{"y": 8,"x": 37,"type": "Snow","notes": ""},
        {"y": 8,"x": 38,"type": "Snow","notes": ""},{"y": 7,"x": 38,"type": "Snow","notes": ""},
        {"y": 6,"x": 38,"type": "Snow","notes": ""},{"y": 6,"x": 37,"type": "Snow","notes": ""},
        {"y": 6,"x": 36,"type": "Snow","notes": ""},{"y": 9,"x": 38,"type": "Snow","notes": ""},
        {"y": 10,"x": 38,"type": "Snow","notes": ""},{"y": 10,"x": 37,"type": "Snow","notes": ""},
        {"y": 10,"x": 36,"type": "Snow","notes": ""},{"y": 10,"x": 35,"type": "Snow","notes": ""}
    ],
    "notes": [],
    "units": [],
    "fow": [ [ False for y in range(100) ] for x in range(100) ]
}


with open("data.json", "r") as f:
    game_data = json.load(f)

# click supported save
#def save(ctx, map_obj):
#    with open(ctx.obj["data_location"], "w") as f:
#        json.dump(map_obj, f, indent=4)

def gen_save(save_loc):
    def save():
        with open(save_loc, "w") as f:
            json.dump(game_data, f, indent=4)
    return save


def start_server(host, port, _gm_password, _password, save_loc):
    global save
    save = gen_save(save_loc) # currey save func

    print("Server url: ws://{0}:{1}".format(host, port))

    global gm_password
    gm_password = _gm_password

    global password
    password = _password
    broadcast_server.start_server(host, port)

if __name__ == "__main__":
    start_server("127.0.0.1", 9000)
