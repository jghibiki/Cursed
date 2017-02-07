from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
import sys
import json
import hashlib
import random
import authentication
import logging
from uuid import uuid4
from authentication import requires_auth, requires_gm_auth

app = Flask(__name__)
CORS(app)

game_data = None
save_callback = None
users = []


######
## Helpers
#####

def _get_user():
    auth = request.authorization
    username = auth.username
    map_name = None
    for user in users:
        if user["username"] == username:
            return user

    return None

######
## Error Handler
#####
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

###
# Routes
###

@app.route("/map/data/", methods=["GET"])
@requires_auth
def get_map(index=None):


    user = _get_user()
    if not user:
        return 'username not set', 400

    name = user["current_map"]
    if not name:
        return 'user current_map not set', 400

    return jsonify(game_data["maps"][name])



@app.route("/map/add", methods=["POST"])
@requires_gm_auth
def add_feature_to_map():
    data = request.json

    # validate request data
    if data is None:
        return 'No payload recieved', 400
    if "y" not in data:
        return 'Payload missing field "y"', 400
    if "x" not in data :
        return 'Payload missing field "x"', 400
    if "type" not in data:
        return 'Playload missing field "type"', 400
    if "notes" not in data:
        return ('Payload midding field "notes"', 400)


    user = _get_user()
    if not user:
        return 'username not set', 400

    map_name = user["current_map"]
    if not map_name:
        return 'user current_map not set', 400


    features = game_data["maps"][map_name]["features"]

    for feature in features:
        if feature["y"] == data["y"] and feature["x"] == data["x"]:
            return ('', 500)

    game_data["maps"][map_name]["features"].append(data)

    data = json.dumps(game_data["maps"][map_name], sort_keys=True).encode("utf-8")
    hsh = hashlib.md5(data).hexdigest()
    game_data["map_hashes"][map_name]["map"] = hsh

    return jsonify({})

@app.route("/map/bulk/add", methods=["POST"])
@requires_gm_auth
def bulk_add_feature_to_map():
    data = request.json

    if data is None:
        return 'No payload recieved', 400

    new_features = data["features"]

    user = _get_user()
    if not user:
        return 'username not set', 400

    map_name = user["current_map"]
    if not map_name:
        return 'user current_map not set', 400

    features = game_data["maps"][map_name]["features"]

    already_exist = []

    for new_feature in new_features:
        for feature in features:
            if feature["y"] == new_feature["y"] and feature["x"] == new_feature["x"]:
                already_exist.append(new_feature)

    new_features = [ feature for feature in new_features if feature not in already_exist ]
    for new_feature in new_features:
        game_data["maps"][map_name]["features"].append(new_feature)

    data = json.dumps(game_data["maps"][map_name], sort_keys=True).encode("utf-8")
    hsh = hashlib.md5(data).hexdigest()
    game_data["map_hashes"][map_name]["map"] = hsh

    return jsonify({})

@app.route('/map/rm', methods=["POST"])
@requires_gm_auth
def rm_feature_from_map():
    data = request.json

    if ( ( data is None ) or
         ( "y" not in data ) or
         ( "x" not in data ) ):
        return ('', 400)

    user = _get_user()
    if not user:
        return 'username not set', 400

    map_name = user["current_map"]
    if not map_name:
        return 'user current_map not set', 400

    features = game_data["maps"][map_name]["features"]
    for feature in features:
        if feature["y"] == data["y"] and feature["x"] == data["x"]:
                features.remove(feature)
                game_data["maps"][map_name]["features"] = features

                data = json.dumps(game_data["maps"][map_name], sort_keys=True).encode("utf-8")
                hsh = hashlib.md5(data).hexdigest()
                game_data["map_hashes"][map_name]["map"] = hsh

                return jsonify({})

    return '', 500

@app.route('/map/new', methods=["POST"])
@requires_gm_auth
def create_new_map():
    data = request.json
    map_name = data["name"]
    max_x = data["width"]
    max_y = data["height"]

    game_data["maps"][map_name] = {
        "max_x": max_x,
        "max_y": max_y,
        "features": [],
        "notes": [],
        "units": [],
        "fow": [ [ False for y in range(max_y) ] for x in range(max_x) ]
    }

@app.route('/map/bulk/rm', methods=["POST"])
@requires_gm_auth
def bulk_rm_feature_from_map():
    data = request.json

    if data is None:
        return ('', 400)

    new_features = data["features"]

    user = _get_user()
    if not user:
        return 'username not set', 400

    map_name = user["current_map"]
    if not map_name:
        return 'user current_map not set', 400

    features = game_data["maps"][map_name]["features"]
    for new_feature in new_features:
        for feature in features:
            if feature["y"] == new_feature["y"] and feature["x"] == new_feature["x"]:
                try:
                    features.remove(feature)
                except:
                    pass

    game_data["maps"][map_name]["features"] = features

    data = json.dumps(game_data["maps"][map_name], sort_keys=True).encode("utf-8")
    hsh = hashlib.md5(data).hexdigest()
    game_data["map_hashes"][map_name]["map"] = hsh

    return jsonify({})


@app.route('/map/update/', methods=["POST"])
@requires_gm_auth
def update_feature():
    data = request.json

    # validate request data
    if data is None:
        return 'No payload recieved', 400
    if "y" not in data:
        return 'Payload missing field "y"', 400
    if "x" not in data :
        return 'Payload missing field "x"', 400
    if "type" not in data:
        return 'Playload missing field "type"', 400
    if "notes" not in data:
        return ('Payload midding field "notes"', 400)

    user = _get_user()
    if not user:
        return 'username not set', 400

    map_name = user["current_map"]
    if not map_name:
        return 'user current_map not set', 400

    features = game_data["maps"][map_name]["features"]
    for idx, feature in enumerate(features):
        if feature["y"] == data["y"] and feature["x"] == data["x"]:
            game_data["maps"][map_name]["features"][idx] = data

            data = json.dumps(game_data["maps"][map_name], sort_keys=True).encode("utf-8")
            hsh = hashlib.md5(data).hexdigest()
            game_data["map_hashes"][map_name]["map"] = hsh

            return jsonify({})


@app.route("/map", methods=["POST"])
@requires_gm_auth
def set_map_name():
    data = request.json
    user_to_change = data["username"]
    new_map = data["map_name"]

    valid_map = False
    for map_name in game_data["maps"].keys():
        if map_name == new_map:
            valid_map = True

    if not valid_map:
        return "Invalid map name", 400

    global users
    for user in users:
        if user["username"] == user_to_change:
            user["current_map"] = new_map

            return jsonify({"result": True})
    return jsonify({"result": False})


@app.route("/map", methods=["GET"])
@requires_auth
def get_map_name():
    return jsonify({"maps": list(game_data["maps"].keys())})


@app.route("/narrative", methods=["GET"])
@requires_gm_auth
def get_narratives():
    narratives = [ nar["name"] for nar in game_data["story"] ]

    return jsonify({"chapters": narratives})

@app.route("/narrative/<int:index>", methods=["GET"])
@requires_gm_auth
def get_narrative_by_index(index):
    return jsonify(game_data["story"][index])

@app.route("/narrative/<int:index>", methods=["POST"])
@requires_gm_auth
def update_narrative_by_index(index):
    data = request.json

    if data is None:
        return 'No payload recieved', 400
    if "name" not in data:
        return 'Payload missing field "name"', 400
    if "text" not in data :
        return 'Payload missing field "text"', 400

    global game_data
    game_data["story"][index] = data

    return jsonify({})


@app.route('/chat', methods=["POST"])
@requires_auth
def add_chat_message():
    data = request.json

    if data is None:
        return 'No payload recieved', 400
    if "sender" not in data:
        return 'Payload missing field "sender"', 400
    if "recipient" not in data:
        return 'Payload missing field "recipient"', 400
    if "message" not in data:
        return 'Payload missing field "message"', 400


    global game_data
    game_data["chat"].append(data)

    data = json.dumps(game_data["chat"], sort_keys=True).encode("utf-8")
    hsh = hashlib.md5(data).hexdigest()
    game_data["global_hashes"]["chat"] = hsh

    return jsonify({})

@app.route('/users', methods=["GET"])
@requires_auth
def get_users():
    return jsonify({"users": users})


@app.route('/users', methods=["POST"])
@requires_auth
def set_user_info():
    data = request.json

    if "username" not in data:
        raise InvalidUsage('Payload missing field "username')
    if "current_map" not in data:
        raise InvalidUsage('Payload missing field "current_map')

    exists = False


    global users
    for user in users:
        if user["username"] == data["username"]:
            exists = True
            break

    if not exists:

        new_user = {}

        new_user["username"] = data["username"]
        new_user["current_map"] = "__staging__"

        auth = request.authorization
        if authentication.gm_password == auth.password:
            new_user["role"] = "gm"
        else:
            new_user["role"] = "pc"

        if new_user["current_map"] == None:
            new_user["current_map"] == "__staging__"


        users.append(new_user)

        data = json.dumps(users, sort_keys=True).encode("utf-8")
        hsh = hashlib.md5(data).hexdigest()
        user_hash = hsh

    return jsonify({})

@app.route('/notes', methods=["GET"])
@requires_auth
def get_notes():
    user = _get_user()
    if not user:
        return 'username not set', 400

    map_name = user["current_map"]
    if not map_name:
        return 'user current_map not set', 400

    return jsonify(game_data["maps"][map_name]["notes"])

#TODO: actually implement set notes (part of the point of interest replacement)
@app.route('/notes', methods=["GET"])
@requires_auth
def set_notes():
    user = _get_user()
    if not user:
        return 'username not set', 400

    map_name = user["current_map"]
    if not map_name:
        return 'user current_map not set', 400

    return jsonify(game_data["maps"][map_name]["notes"])

@app.route('/chat/<username>', methods=["GET"])
@requires_auth
def get_chat_messages(username):
    all_messages = game_data["chat"]
    messages = []

    for message in all_messages:
        if ( message["recipient"] == username or
             message["sender"] == username or
             message["recipient"] == None ):
            messages.append(message)

    return jsonify({ "messages": messages })

@app.route('/chat/<username>/hash', methods=["GET"])
@requires_auth
def get_chat_hash(username):
    all_messages = game_data["chat"]
    messages = []

    #for message in all_messages:
    #    if ( message["recipient"] == username or
    #         message["sender"] == username or
    #         message["recipient"] == None ):
    #        messages.append(message)

    #data = json.dumps(messages, sort_keys=True).encode("utf-8")
    #hash = hashlib.md5(data).hexdigest()

    return jsonify({ "hash": chat_hash })

@app.route('/hash', methods=["GET"])
@requires_auth
def get_hashes():
    user = _get_user()
    if not user:
        return 'username not set', 400

    map_name = user["current_map"]
    if not map_name:
        return 'user current_map not set', 400

    return jsonify({
        "map": game_data["map_hashes"][map_name]["map"],
        "fow": game_data["map_hashes"][map_name]["fow"],
        "unit": game_data["map_hashes"][map_name]["unit"],
        "chat": game_data["global_hashes"]["chat"],
        "users": game_data["global_hashes"]["users"]
    })

@app.route('/save', methods=["GET"])
@requires_gm_auth
def save_data():
    save_callback(game_data)
    return jsonify({})

@app.route('/fow/add', methods=["POST"])
@requires_gm_auth
def add_fow():
    data = request.json

    if "x" not in data:
        return 'Payload missing field "x"', 400
    if "y" not in data:
        return 'Payload missing field "y"', 400

    x = data["x"]
    y = data["y"]

    user = _get_user()
    if not user:
        return 'username not set', 400

    map_name = user["current_map"]
    if not map_name:
        return 'user current_map not set', 400

    global dame_data
    game_data["maps"][map_name]["fow"][x][y] = True

    data = json.dumps(game_data["maps"][map_name]["fow"], sort_keys=True).encode("utf-8")
    hsh = hashlib.md5(data).hexdigest()
    game_data["map_hashes"][map_name]["fow"] = hsh

    return jsonify({})

@app.route('/fow/bulk/add', methods=["POST"])
@requires_gm_auth
def bulk_add_fow():
    data = request.json

    global game_data
    for row in data["fow"]:
        game_data["maps"][current_map]["fow"][row["x"]][row["y"]] = True

    user = _get_user()
    if not user:
        return 'username not set', 400

    map_name = user["current_map"]
    if not map_name:
        return 'user current_map not set', 400

    data = json.dumps(game_data["maps"][current_map]["fow"], sort_keys=True).encode("utf-8")
    hsh = hashlib.md5(data).hexdigest()
    game_data["map_hashes"][map_name]["fow"] = hsh

    return jsonify({})


@app.route('/fow/rm', methods=["POST"])
@requires_gm_auth
def rm_fow():
    data = request.json

    if "x" not in data:
        return 'Payload missing field "x"', 400
    if "y" not in data:
        return 'Payload missing field "y"', 400

    x = data["x"]
    y = data["y"]

    user = _get_user()
    if not user:
        return 'username not set', 400

    map_name = user["current_map"]
    if not map_name:
        return 'user current_map not set', 400

    global game_data
    game_data["maps"][map_name]["fow"][x][y] = False

    data = json.dumps(game_data["maps"][map_name]["fow"], sort_keys=True).encode("utf-8")
    hsh = hashlib.md5(data).hexdigest()
    game_data["map_hashes"][map_name]["fow"] = hsh

    return jsonify({})

@app.route('/fow/bulk/rm', methods=["POST"])
@requires_gm_auth
def bulk_rm_fow():
    data = request.json

    user = _get_user()
    if not user:
        return 'username not set', 400

    map_name = user["current_map"]
    if not map_name:
        return 'user current_map not set', 400

    global dame_data
    for row in data["fow"]:
        game_data["maps"][map_name]["fow"][row["x"]][row["y"]] = False

    data = json.dumps(game_data["maps"][map_name]["fow"], sort_keys=True).encode("utf-8")
    hsh = hashlib.md5(data).hexdigest()
    game_data["map_hashes"][map_name]["fow"] = hsh

    return jsonify({})


@app.route('/fow', methods=["GET"])
@requires_auth
def get_fow():

    user = _get_user()
    if not user:
        return 'username not set', 400

    map_name = user["current_map"]
    if not map_name:
        return 'user current_map not set', 400

    return jsonify({
        "fow": game_data["maps"][map_name]["fow"]
    })

@app.route('/fow/toggle', methods=["GET"])
@requires_gm_auth
def toggle_fow():

    user = _get_user()
    if not user:
        return 'username not set', 400

    map_name = user["current_map"]
    if not map_name:
        return 'user current_map not set', 400

    global game_data
    initial = not game_data["maps"][map_name]["fow"][0][0]
    for x in range(0, game_data["maps"][map_name]["max_x"]):
        for y in range(0, game_data["maps"][map_name]["max_y"]):
            game_data["maps"][map_name]["fow"][x][y] = initial

    data = json.dumps(game_data["maps"][map_name]["fow"], sort_keys=True).encode("utf-8")
    hsh = hashlib.md5(data).hexdigest()
    game_data["map_hashes"][map_name]["fow"] = hsh

    return jsonify({})

@app.route('/fow/fill', methods=["GET"])
@requires_gm_auth
def all_fow():

    user = _get_user()
    if not user:
        return 'username not set', 400

    map_name = user["current_map"]
    if not map_name:
        return 'user current_map not set', 400

    global game_data
    for x in range(0, game_data["maps"][map_name]["max_x"]):
        for y in range(0, game_data["maps"][map_name]["max_y"]):
            game_data["maps"][map_name]["fow"][x][y] = True

    data = json.dumps(game_data["maps"][map_name]["fow"], sort_keys=True).encode("utf-8")
    hsh = hashlib.md5(data).hexdigest()
    game_data["map_hashes"][map_name]["fow"] = hsh

    return jsonify({})

@app.route('/fow/clear', methods=["GET"])
@requires_gm_auth
def none_fow():

    user = _get_user()
    if not user:
        return 'username not set', 400

    map_name = user["current_map"]
    if not map_name:
        return 'user current_map not set', 400

    global game_data
    for x in range(0, game_data["maps"][map_name]["max_x"]):
        for y in range(0, game_data["maps"][map_name]["max_y"]):
            game_data["maps"][map_name]["fow"][x][y] = False

    data = json.dumps(game_data["maps"][current_map]["fow"], sort_keys=True).encode("utf-8")
    hsh = hashlib.md5(data).hexdigest()
    game_data["map_hashes"][map_name]["fow"] = hsh

    return jsonify({})

@app.route('/unit/add', methods=["POST"])
@requires_gm_auth
def add_unit():
    data = request.json

    if "x" not in data:
        return 'Payload missing field "x"', 400
    if "y" not in data:
        return 'Payload missing field "y"', 400
    if "name" not in data:
        return 'Payload missing field "name"', 400
    if "max_health" not in data:
        return 'Payload missing field "max_health"', 400
    if "current_health" not in data:
        return 'Payload missing field "current_health"', 400
    if "controller" not in data:
        return 'Payload missing field "controller"', 400
    if "type" not in data:
        return 'Payload missing field "type"', 400

    data["id"] = str(uuid4())

    user = _get_user()
    if not user:
        return 'username not set', 400

    map_name = user["current_map"]
    if not map_name:
        return 'user current_map not set', 400

    global game_data
    game_data["maps"][map_name]["units"].append(data)

    data = json.dumps(game_data["maps"][current_map]["units"], sort_keys=True).encode("utf-8")
    game_data["map_hashes"][map_name]["units"] = hashlib.md5(data).hexdigest()

    return jsonify({})

@app.route('/unit/rm', methods=["POST"])
@requires_gm_auth
def rm_unit():
    data = request.json

    if "id" not in data:
        return 'Payload missing field "id"', 400

    user = _get_user()
    if not user:
        return 'username not set', 400

    map_name = user["current_map"]
    if not map_name:
        return 'user current_map not set', 400

    global game_data
    units = game_data["maps"][map_name]["units"]

    for unit in units:
        if unit["id"] == data["id"]:
            game_data["maps"][map_name]["units"].remove(unit)
            break

    data = json.dumps(game_data["maps"][current_map]["units"], sort_keys=True).encode("utf-8")
    game_data["map_hashes"][map_name]["units"] = hashlib.md5(data).hexdigest()

    return jsonify({})

@app.route('/unit/update', methods=["POST"])
@requires_auth
def update_unit():
    data = request.json

    if "x" not in data:
        return 'Payload missing field "x"', 400
    if "y" not in data:
        return 'Payload missing field "y"', 400
    if "name" not in data:
        return 'Payload missing field "name"', 400
    if "max_health" not in data:
        return 'Payload missing field "max_health"', 400
    if "current_health" not in data:
        return 'Payload missing field "current_health"', 400
    if "controller" not in data:
        return 'Payload missing field "controller"', 400
    if "type" not in data:
        return 'Payload missing field "type"', 400
    if "id" not in data:
        return 'Payload missing field "id"', 400

    global game_data

    user = _get_user()
    if not user:
        return 'username not set', 400

    map_name = user["current_map"]
    if not map_name:
        return 'user current_map not set', 400

    for i in range(len(game_data["maps"][map_name]["units"])):
        if game_data["maps"][map_name]["units"][i]["id"] == data["id"]:
            game_data["maps"][map_name]["units"][i] = data
            break

    data = json.dumps(game_data["maps"][map_name]["units"], sort_keys=True).encode("utf-8")
    game_data["map_hashes"][map_name]["units"] = hashlib.md5(data).hexdigest()

    return jsonify({})

@app.route('/unit', methods=["GET"])
@requires_auth
def get_units():

    user = _get_user()
    if not user:
        return 'username not set', 400

    map_name = user["current_map"]
    if not map_name:
        return 'user current_map not set', 400

    units = game_data["maps"][map_name]["units"]
    return jsonify({"units": units})



def run(data, port, host, gm_passwd, passwd, map_name, save):
    global game_data
    game_data = data

    global save_callback
    save_callback = save

    # add staging map
    game_data["maps"]["__staging__"] = {
        "max_x": 100,
        "max_y": 100,
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

    game_data["map_hashes"] = {}

    for map in game_data["maps"].keys():

        data = json.dumps(game_data["maps"][map], sort_keys=True).encode("utf-8")
        map_hash = hashlib.md5(data).hexdigest()

        data = json.dumps(game_data["maps"][map]["fow"], sort_keys=True).encode("utf-8")
        fow_hash = hashlib.md5(data).hexdigest()

        data = json.dumps(game_data["maps"][map]["units"], sort_keys=True).encode("utf-8")
        unit_hash = hashlib.md5(data).hexdigest()

        game_data["map_hashes"][map] = {
            "map": map_hash,
            "fow": fow_hash,
            "unit": unit_hash,
        }

    data = json.dumps(users, sort_keys=True).encode("utf-8")
    hsh = hashlib.md5(data).hexdigest()
    user_hash = hsh

    data = json.dumps(game_data["chat"], sort_keys=True).encode("utf-8")
    chat_hash = hashlib.md5(data).hexdigest()

    game_data["global_hashes"] = {
        "users": user_hash,
        "chat": chat_hash
    }

    tmp = "%s%s%s%s" % (random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))
    authentication.gm_password = gm_passwd if gm_passwd else tmp
    print("GM Password: %s" % authentication.gm_password)

    tmp = "%s%s%s%s" % (random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))
    authentication.password = passwd if passwd else tmp
    print("PC Password: %s" % authentication.password)

    app.run(port=port, host=host, threaded=True, debug=True)
