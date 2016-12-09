from flask import Flask, jsonify, request
import sys
import json
import hashlib
import random
import authentication
import logging
from uuid import uuid4
from authentication import requires_auth, requires_gm_auth

app = Flask(__name__)

game_data = None
save_callback = None
current_map = None
map_hash = None
feature_hashes = []
chat_hash = None
fow_hash = None
unit_hash = None


@app.route("/map/data/", methods=["GET"])
@app.route("/map/data/<index>/", methods=["GET"])
@requires_auth
def get_map(index=None):

    name = current_map

    if not index:
        return jsonify(
                game_data["maps"][name])

    return jsonify(game_data["maps"][name]["features"][index])



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

    name = current_map

    features = game_data["maps"][name]["features"]

    for feature in features:
        if feature["y"] == data["y"] and feature["x"] == data["x"]:
            return ('', 500)

    game_data["maps"][name]["features"].append(data)

    global map_hash
    data = json.dumps(game_data["maps"][name], sort_keys=True).encode("utf-8")
    hsh = hashlib.md5(data).hexdigest()
    map_hash = hsh

    global feature_hashes
    json_str = json.dumps(feature, sort_keys=True).encode("utf-8")
    h = hashlib.md5(json_str).hexdigest()
    feature_hashes.append(h)

    return jsonify({})

@app.route('/map/rm', methods=["POST"])
@app.route('/map/rm/<name>', methods=["POST"])
def rm_feature_from_map(name=None):
    data = request.json

    if ( ( data is None ) or
         ( "y" not in data ) or
         ( "x" not in data ) ):
        return ('', 400)

    if not name:
        name = current_map

    features = game_data["maps"][name]["features"]
    for feature in features:
        if feature["y"] == data["y"] and feature["x"] == data["x"]:
                features.remove(feature)
                game_data["maps"][name]["features"] = features

                global map_hash
                data = json.dumps(game_data["maps"][name], sort_keys=True).encode("utf-8")
                hsh = hashlib.md5(data).hexdigest()
                map_hash = hsh

                global feature_hashes
                json_str = json.dumps(feature, sort_keys=True).encode("utf-8")
                h = hashlib.md5(json_str).hexdigest()
                feature_hashes.remove(h)

                return jsonify({})

    return '', 500

@app.route('/map/update/', methods=["POST"])
@app.route('/map/update/<name>', methods=["POST"])
def update_feature(name=None):
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

    if not name:
        name = current_map

    features = game_data["maps"][name]["features"]
    for idx, feature in enumerate(features):
        if feature["y"] == data["y"] and feature["x"] == data["x"]:
            game_data["maps"][name]["features"][idx] = data

    return jsonify({})



@app.route("/map", methods=["POST"])
def set_map_name():
    global current_map
    data = request.json
    current_map = data["map_name"]

    # generate feature hashes
    global feature_hashes
    feature_hashes = []
    for feature in game_data["maps"][current_map]["features"]:
        json_str = json.dumps(feature, sort_keys=True).encode("utf-8")
        h = hashlib.md5(json_str).hexdigest()
        feature_hashes.append(h)

    return jsonify({})


@app.route("/map", methods=["GET"])
@requires_auth
def get_map_name():
    return jsonify({"map_name": current_map})


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

    global chat_hash
    data = json.dumps(game_data["chat"], sort_keys=True).encode("utf-8")
    chat_hash = hashlib.md5(data).hexdigest()

    return jsonify({})

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
    return jsonify({
        "map": map_hash,
        "features": feature_hashes,
        "chat": chat_hash,
        "fow": fow_hash,
        "unit": unit_hash
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

    global dame_data
    game_data["maps"][current_map]["fow"][x][y] = True

    global fow_hash
    data = json.dumps(game_data["maps"][current_map]["fow"], sort_keys=True).encode("utf-8")
    hsh = hashlib.md5(data).hexdigest()
    fow_hash = hsh

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

    global dame_data
    game_data["maps"][current_map]["fow"][x][y] = False

    global fow_hash
    data = json.dumps(game_data["maps"][current_map]["fow"], sort_keys=True).encode("utf-8")
    hsh = hashlib.md5(data).hexdigest()
    fow_hash = hsh

    return jsonify({})

@app.route('/fow', methods=["GET"])
@requires_auth
def get_fow():

    return jsonify({
        "fow": game_data["maps"][current_map]["fow"]
    })

@app.route('/fow/toggle', methods=["GET"])
@requires_gm_auth
def toggle_fow():

    global dame_data
    initial = not game_data["maps"][current_map]["fow"][0][0]
    for x in range(0, game_data["maps"][current_map]["max_x"]):
        for y in range(0, game_data["maps"][current_map]["max_y"]):
            game_data["maps"][current_map]["fow"][x][y] = initial

    global fow_hash
    data = json.dumps(game_data["maps"][current_map]["fow"], sort_keys=True).encode("utf-8")
    hsh = hashlib.md5(data).hexdigest()
    fow_hash = hsh

    return jsonify({})

@app.route('/fow/fill', methods=["GET"])
@requires_gm_auth
def all_fow():

    global dame_data
    for x in range(0, game_data["maps"][current_map]["max_x"]):
        for y in range(0, game_data["maps"][current_map]["max_y"]):
            game_data["maps"][current_map]["fow"][x][y] = True

    global fow_hash
    data = json.dumps(game_data["maps"][current_map]["fow"], sort_keys=True).encode("utf-8")
    hsh = hashlib.md5(data).hexdigest()
    fow_hash = hsh

    return jsonify({})

@app.route('/fow/clear', methods=["GET"])
@requires_gm_auth
def none_fow():

    global dame_data
    for x in range(0, game_data["maps"][current_map]["max_x"]):
        for y in range(0, game_data["maps"][current_map]["max_y"]):
            game_data["maps"][current_map]["fow"][x][y] = False

    global fow_hash
    data = json.dumps(game_data["maps"][current_map]["fow"], sort_keys=True).encode("utf-8")
    hsh = hashlib.md5(data).hexdigest()
    fow_hash = hsh

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

    global game_data
    game_data["maps"][current_map]["units"].append(data)

    global unit_hash
    data = json.dumps(game_data["maps"][current_map]["units"], sort_keys=True).encode("utf-8")
    unit_hash = hashlib.md5(data).hexdigest()

    return jsonify({})

@app.route('/unit/rm', methods=["POST"])
@requires_gm_auth
def rm_unit():
    data = request.json

    if "id" not in data:
        return 'Payload missing field "id"', 400

    global game_data
    units = game_data["maps"][current_map]["units"]

    for unit in units:
        if unit["id"] == data["id"]:
            game_data["maps"][current_map]["units"].remove(unit)
            break

    global unit_hash
    data = json.dumps(game_data["maps"][current_map]["units"], sort_keys=True).encode("utf-8")
    unit_hash = hashlib.md5(data).hexdigest()

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

    for i in range(len(game_data["maps"][current_map]["units"])):
        if game_data["maps"][current_map]["units"][i]["id"] == data["id"]:
            game_data["maps"][current_map]["units"][i] = data
            break

    global unit_hash
    a = unit_hash
    data = json.dumps(game_data["maps"][current_map]["units"], sort_keys=True).encode("utf-8")
    unit_hash = hashlib.md5(data).hexdigest()

    return jsonify({})

@app.route('/unit', methods=["GET"])
@requires_auth
def get_units():
    units = game_data["maps"][current_map]["units"]
    return jsonify({"units": units})



def run(data, port, host, gm_passwd, passwd, map_name, save):
    global game_data
    game_data = data

    global save_callback
    save_callback = save

    global current_map
    current_map = map_name


    # calculate map hash
    global map_hash
    data = json.dumps(game_data["maps"][map_name], sort_keys=True).encode("utf-8")
    hsh = hashlib.md5(data).hexdigest()
    map_hash = hsh

    # calculate fow hash
    global fow_hash
    data = json.dumps(game_data["maps"][current_map]["fow"], sort_keys=True).encode("utf-8")
    hsh = hashlib.md5(data).hexdigest()
    fow_hash = hsh

    global unit_hash
    data = json.dumps(game_data["maps"][current_map]["units"], sort_keys=True).encode("utf-8")
    unit_hash = hashlib.md5(data).hexdigest()

    global chat_hash
    data = json.dumps(game_data["chat"], sort_keys=True).encode("utf-8")
    chat_hash = hashlib.md5(data).hexdigest()

    tmp = "%s%s%s%s" % (random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))
    authentication.gm_password = gm_passwd if gm_passwd else tmp
    print("GM Password: %s" % authentication.gm_password)

    tmp = "%s%s%s%s" % (random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))
    authentication.password = passwd if passwd else tmp
    print("PC Password: %s" % authentication.password)

    app.run(port=port, host=host, threaded=True, debug=False)
