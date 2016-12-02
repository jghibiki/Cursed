from flask import Flask, jsonify, request
import sys
import json
import hashlib
import random
import authentication
import logging
from authentication import requires_auth, requires_gm_auth

app = Flask(__name__)

game_data = None
save_callback = None
current_map = None
map_hash = None
feature_hashes = []
chat_hash = None


@app.route("/map/data/", methods=["GET"])
@app.route("/map/data/<index>/", methods=["GET"])
@requires_auth
def get_map(index=None):

    name = current_map

    if not index:
        return jsonify(
                game_data["maps"][name])

    return jsonify(game_data["maps"][name]["features"][index])


@app.route("/map/hash/", methods=["GET"])
@requires_auth
def get_map_hash():
    name = current_map

    data = json.dumps(game_data["maps"][name], sort_keys=True).encode("utf-8")
    hsh = hashlib.md5(data).hexdigest()

    global map_hash
    map_hash = hsh

    return jsonify({"hash": hsh, "features": feature_hashes})

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

    features.append(data)
    game_data["maps"][name]["features"] = features

    json_str = json.dumps(feature, sort_keys=True).encode("utf-8")
    h = hashlib.md5(json_str).hexdigest()
    global feature_hashes
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

                json_str = json.dumps(feature, sort_keys=True).encode("utf-8")
                h = hashlib.md5(json_str).hexdigest()
                global feature_hashes
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
def get_hashes():
    return jsonify({
        "map": map_hash,
        "features": feature_hashes,
        "chat": chat_hash
    })

@app.route('/save', methods=["GET"])
def save_data():
    save_callback(game_data)
    return jsonify({})


def run(data, port, host, gm_passwd, passwd, map_name, save):
    global game_data
    game_data = data

    global save_callback
    save_callback = save

    global current_map
    current_map = map_name

    data = json.dumps(game_data["maps"][map_name], sort_keys=True).encode("utf-8")
    hsh = hashlib.md5(data).hexdigest()

    global map_hash
    map_hash = hsh

    tmp = "%s%s%s%s" % (random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))
    authentication.gm_password = gm_passwd if gm_passwd else tmp
    print("GM Password: %s" % authentication.gm_password)

    tmp = "%s%s%s%s" % (random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))
    authentication.password = passwd if passwd else tmp
    print("PC Password: %s" % authentication.password)

    app.run(port=port, host=host, threaded=True, debug=False)
