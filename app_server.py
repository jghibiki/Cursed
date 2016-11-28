from flask import Flask, jsonify
import json
import hashlib
import random
import authentication
from authentication import requires_auth

app = Flask(__name__)

game_data = None
current_map = None

@app.route("/")
def hello():
    return "Hello World"

@app.route("/map/data/<name>", methods=["GET"])
@requires_auth
def get_map(name):
    return jsonify(
            game_data["maps"][name])

@app.route("/map/hash/<name>", methods=["GET"])
@requires_auth
def get_map_hash(name):
    data = json.dumps(game_data["maps"][name], sort_keys=True)
    hsh = hashlib.md5(data.encode("utf-8")).hexdigest()
    return jsonify({"hash": hsh})

@app.route("/map", methods=["GET"])
@requires_auth
def get_map_name():
    return jsonify({"map_name": current_map})

def run(data, port, host, gm_passwd, passwd):
    global game_data
    game_data = data

    global current_map
    current_map = "test" # TODO: replace this to require gm to access first and set current map

    tmp = "%s%s%s%s" % (random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))
    authentication.gm_password = gm_passwd if gm_passwd else tmp
    print("GM Password: %s" % authentication.gm_password)

    tmp = "%s%s%s%s" % (random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))
    authentication.password = passwd if passwd else tmp
    print("PC Password: %s" % authentication.password)

    app.run(port=port, host=host)
