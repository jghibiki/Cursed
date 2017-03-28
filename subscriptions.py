import magic

##########################
# User Operations        #
##########################

def getUsers(client, req):
    """ Get list of users and public data about them"""
    client.sendTarget(req["id"], key="get.users", payload={"payload": magic.users})

def moveUser(client, req):
    if "username" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="move.user",
                payload={"msg": "Request details missing \"username\""})
        return False
    username = req["details"]["username"]

    if "map_name" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="move.user",
                payload={"msg": "Request details missing \"map_name\""})
        return False
    map_name = req["details"]["map_name"]

    user = _getUserInfo(username=username)
    if not user:
        client.sendTarget(
            req["id"],
            type="error",
            key="move.user",
            payload={
                "msg": "User with id \"{0}\" has not been registered.".format(req["id"])
        })
        return False


    if map_name not in set(magic.game_data["maps"].keys()):
        client.sendTarget(
                req["id"],
                type="error",
                key="move.user",
                payload={
                    "msg": "Map with name \"{0}\" does not exist."
                        .format(new_map_name)})
        return False

    user["current_map"] = map_name
    client.sendTarget(
            req["id"],
            type="acknowledge",
            key="move.user",
            payload={})
    return True



def registerUser(client, req):
    if "username" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="register.user",
                payload={"msg": "Request details missing \"username\""})
        return False
    new_username = req["details"]["username"]

    if "current_map" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="register.user",
                payload={"msg": "Request details missing \"current_map\""})
        return False

    current_map = req["details"]["current_map"]

    exists = False

    for user in magic.users:
        if user["username"] == new_username:
            exists = True
            break

    if not exists:
        new_user = {}
        new_user["username"] = new_username
        new_user["current_map"] = current_map
        new_user["client_id"] = req["id"]

        if req["password"] == magic.gm_password:
            new_user["role"] = "gm"
        elif req["password"] == magic.password:
            new_user["role"] = "pc"

        if new_user["current_map"] == None:
            new_user["current_map"] = "__staging__"

        magic.users.append(new_user)
        client.sendTarget(
                req["id"],
                type="acknowledge",
                key="register.user",
                payload={})
        return True

    else:
        # reassociate user with client
        for user in magic.users:
            if user["username"] == new_username:
                user["client_id"] = req["id"]

        client.sendTarget(
                req["id"],
                type="acknowledge",
                key="register.user",
                payload={})
        return True

##########################
# Chat Operations        #
##########################

def getChat(client, req):
    username = None

    for user in magic.users:
        if user["client_id"] == req["id"]:
            username = user["username"]
            break

    if username:
        all_messages = magic.game_data["chat"]

        messages = []

        for msg in all_messages:
            if ( msg["recipient"] == username or
                 msg["sender"] == username or
                 msg["recipient"] == None ):
                 messages.append(msg)

        client.sendTarget(
                req["id"],
                key="get.chat",
                payload={"payload": messages})
        return True
    return False


def addChatMessage(client, req):
    if "sender" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="register.user",
                payload={"msg": "Request details missing \"sender\""})
        return False
    sender = req["details"]["sender"]

    if "message" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="register.user",
                payload={"msg": "Request details missing \"message\""})
        return False
    message = req["details"]["message"]

    recipient = req["details"]["recipient"] if "recipient" in req["details"] else None
    persona = req["details"]["persona"] if "persona" in req["details"] else None

    magic.game_data["chat"].append({
        "sender": sender,
        "recipient": recipient,
        "message": message,
        "persona": persona
    })

    return True

def clearChat(client, req):
    magic.game_data["chat"] = []
    return True




##########################
# Map Operations         #
##########################

def listMaps(client, req):
    maps = list(magic.game_data["maps"].keys())
    client.sendTarget(req["id"], key="list.maps", payload={"payload": maps})


def addMap(client, req):
    if "name" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="add.map",
                payload={"msg": "Request details missing \"name\""})
        return False
    new_map_name = req["details"]["name"]

    if "width" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="add.map",
                payload={"msg": "Request details missing \"width\""})
        return False
    width = req["details"]["width"]

    if "height" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="add.map",
                payload={"msg": "Request details missing \"height\""})
        return False
    height = req["details"]["height"]


    for map_name in magic.game_data["maps"].keys():
        if map_name == new_map_name:
            client.sendTarget(
                    req["id"],
                    type="error",
                    key="add.map",
                    payload={
                        "msg": "Map with name \"{0}\" already exists."
                            .format(new_map_name)})
            return False

    magic.game_data["maps"][new_map_name] = {
        "max_x": width,
        "max_y": height,
        "features": [],
        "notes": [],
        "units": [],
        "fow": [ [ False for y in range(height) ] for x in range(width) ]
    }
    client.sendTarget(
            req["id"],
            type="acknowledge",
            key="add.map",
            payload={})
    return True

def removeMap(client, req):
    if "name" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="remove.map",
                payload={"msg": "Request details missing \"name\""})
        return False
    map_to_remove = req["details"]["name"]

    exists = False

    for map_name in magic.game_data["maps"].keys():
        if map_name == map_to_remove:
            exists = True
            break

    if exists:
        del magic.game_data["maps"][map_to_remove]
        client.sendTarget(
                req["id"],
                type="acknowledge",
                key="remove.map",
                payload={})
        return True
    else:
        client.sendTarget(
                req["id"],
                type="error",
                key="remove.map",
                payload={
                    "msg": "Map with name \"{0}\" does not exist."
                        .format(new_map_name)})
        return False

def renameMap(client, req):
    if "current_name" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="rename.map",
                payload={"msg": "Request details missing \"current_name\""})
        return False
    current_name = req["details"]["current_name"]

    if "new_name" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="rename.map",
                payload={"msg": "Request details missing \"new_name\""})
        return False
    new_name = req["details"]["new_name"]

    print(current_name, new_name)
    if current_name == new_name:
        client.sendTarget(
                req["id"],
                type="error",
                key="rename.map",
                payload={
                    "msg": "Current map name and new map name cannot be the same."})
        return False

    exists = False
    for map_name in magic.game_data["maps"].keys():
        if map_name == current_name:
            exists = True
            break

    if exists:
        magic.game_data["maps"][new_name] = magic.game_data["maps"][current_name]
        del magic.game_data["maps"][current_name]
        client.sendTarget(
                req["id"],
                type="acknowledge",
                key="rename.map",
                payload={})
        return True
    else:
        client.sendTarget(
                req["id"],
                type="error",
                key="rename.map",
                payload={
                    "msg": "Map with name \"{0}\" does not exist."
                        .format(new_map_name)})
        return False

def getMap(client, req):
    user = _getUserInfo(id=req["id"])

    if user:
        if user["current_map"] in magic.game_data["maps"]:
            data = magic.game_data["maps"][user["current_map"]]
            client.sendTarget(req["id"], key="get.map", payload={"payload": data})
            return True
        else:
            client.sendTarget(
                req["id"],
                type="error",
                key="get.map",
                payload={
                    "msg": "User \"{0}\" is on map \"{1}\", however this map could not be found.".format(user["username"], user["current_map"])
            })

        return False
    else:
        client.sendTarget(
            req["id"],
            type="error",
            key="get.map",
            payload={
                "msg": "User with id \"{0}\" has not been registered.".format(req["id"])
        })
        return False

#
# Note Operations
#
def getMapNotes(client, req):

    user = _getUserInfo(id=req["id"])
    if user:
        if user["current_map"] in magic.game_data["maps"]:
            notes = magic.game_data["maps"][user["current_map"]]["notes"]
            client.sendTarget(req["id"], key="get.map.notes", payload={"payload": notes})
            return True
        else:
            client.sendTarget(
                req["id"],
                type="error",
                key="get.map.notes",
                payload={
                    "msg": "User \"{0}\" is on map \"{1}\", however this map could not be found.".format(user["username"], user["current_map"])
            })

        return False
    else:
        client.sendTarget(
            req["id"],
            type="error",
            key="get.map.notes",
            payload={
                "msg": "User with id \"{0}\" has not been registered.".format(req["id"])
        })
        return False

def addMapNote(client, req):
    # x and y should be optional
    x = req["details"]["x"] if "x" in req["details"] else None
    y = req["details"]["y"] if "y" in req["details"] else None

    if "text" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="add.map.notes",
                payload={"msg": "Request details missing \"text\""})
        return False
    text = req["details"]["text"]

    if "id" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="add.map.note",
                payload={"msg": "Request details missing \"id\""})
        return False
    id = req["details"]["id"]

    user = _getUserInfo(id=req["id"])
    if not user:
        client.sendTarget(
            req["id"],
            type="error",
            key="add.map.note",
            payload={
                "msg": "User with id \"{0}\" has not been registered.".format(req["id"])
        })
        return False

    if user["current_map"] not in magic.game_data["maps"]:
        client.sendTarget(
            req["id"],
            type="error",
            key="add.map.note",
            payload={
                "msg": "User \"{0}\" is on map \"{1}\", however this map could not be found.".format(user["username"], user["current_map"])
        })

        return False

    magic.game_data[user["current_map"]]["notes"].push({
        "x": x,
        "y": y,
        "text": text,
        "id": id
    })

    client.sendTarget(
            req["id"],
            type="acknowledge",
            key="add.map.notes",
            payload={})

    return True

def removeMapNote(client, req):

    if "id" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="remove.map.note",
                payload={"msg": "Request details missing \"id\""})
        return False
    id = req["details"]["id"]

    user = _getUserInfo(id=req["id"])
    if not user:
        client.sendTarget(
            req["id"],
            type="error",
            key="remove.map.note",
            payload={
                "msg": "User with id \"{0}\" has not been registered.".format(req["id"])
        })
        return False

    if user["current_map"] not in magic.game_data["maps"]:
        client.sendTarget(
            req["id"],
            type="error",
            key="remove.map.note",
            payload={
                "msg": "User \"{0}\" is on map \"{1}\", however this map could not be found.".format(user["username"], user["current_map"])
        })

        return False

    notes = magic.game_data[user["current_map"]]["notes"]
    for note in notes:
        if note["id"] == id:
            notes.remove(note)

            client.sendTarget(
                    req["id"],
                    type="acknowledge",
                    key="add.map.note",
                    payload={})
            return True

    client.sendTarget(
        req["id"],
        type="error",
        key="remove.map.note",
        payload={
            "msg": "Note with id \"{0}\" on map \"{1}\".".format(id, user["current_map"])
    })
    return False


def modifyMapNote(client, req):
    x = req["details"]["x"] if "x" in req["details"] else None
    y = req["details"]["y"] if "y" in req["details"] else None

    if "text" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="modify.map.note",
                payload={"msg": "Request details missing \"text\""})
        return False
    id = req["details"]["text"]

    if "id" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="modify.map.note",
                payload={"msg": "Request details missing \"id\""})
        return False
    id = req["details"]["id"]

    user = _getUserInfo(id=req["id"])
    if not user:
        client.sendTarget(
            req["id"],
            type="error",
            key="modify.map.note",
            payload={
                "msg": "User with id \"{0}\" has not been registered.".format(req["id"])
        })
        return False

    if user["current_map"] not in magic.game_data["maps"]:
        client.sendTarget(
            req["id"],
            type="error",
            key="modiy.map.note",
            payload={
                "msg": "User \"{0}\" is on map \"{1}\", however this map could not be found.".format(user["username"], user["current_map"])
        })

        return False

    notes = magic.game_data[user["current_map"]]["notes"]
    for note in notes:
        if note["id"] == id:
            note["text"] = text
            note["x"] = x
            note["y"] = y

            client.sendTarget(
                    req["id"],
                    type="acknowledge",
                    key="modify.map.note",
                    payload={})
            return True

    client.sendTarget(
        req["id"],
        type="error",
        key="modify.map.note",
        payload={
            "msg": "Note with id \"{0}\" on map \"{1}\".".format(id, user["current_map"])
    })
    return False

#
# Feature Operations
#

def addMapFeature(client, req):
    if "x" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="add.map.feature",
                payload={"msg": "Request details missing \"x\""})
        return False
    x = req["details"]["x"]

    if "y" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="add.map.feature",
                payload={"msg": "Request details missing \"y\""})
        return False
    y = req["details"]["y"]

    if "type" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="add.map.feature",
                payload={"msg": "Request details missing \"type\""})
        return False
    type = req["details"]["type"]


    user = _getUserInfo(id=req["id"])

    if user:
        if user["current_map"] in magic.game_data["maps"]:

            features = magic.game_data["maps"][user["current_map"]]["features"]

            # check if feature already exists here if so error out
            for feature in features:
                if feature["y"] == y and feature["x"] == x:
                    client.sendTarget(
                            req["id"],
                            type="error",
                            key="add.map.feature",
                            payload={
                                "msg": "Feature already exists at ({0}, {1})"
                                     .format(x, y)})
                    return False

            features.append({
                "type": type,
                "x": x,
                "y": y
            })

            client.sendTarget(
                    req["id"],
                    type="acknowledge",
                    key="add.map.feature",
                    payload={})

            return True
        else:
            client.sendTarget(
                req["id"],
                type="error",
                key="add.map.feature",
                payload={
                    "msg": "User \"{0}\" is on map \"{1}\", however this map could not be found.".format(user["username"], user["current_map"])
            })

        return False
    else:
        client.sendTarget(
            req["id"],
            type="error",
            key="add.map.feature",
            payload={
                "msg": "User with id \"{0}\" has not been registered.".format(req["id"])
        })
        return False


def removeMapFeature(client, req):
    if "x" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="remove.map.feature",
                payload={"msg": "Request details missing \"x\""})
        return False
    x = req["details"]["x"]

    if "y" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="remove.map.feature",
                payload={"msg": "Request details missing \"y\""})
        return False
    y = req["details"]["y"]

    user = _getUserInfo(id=req["id"])

    if user:
        if user["current_map"] in magic.game_data["maps"]:

            features = magic.game_data["maps"][user["current_map"]]["features"]

            # check if feature already exists here if so error out
            for feature in features:
                if feature["y"] == y and feature["x"] == x:
                    features.pop(features.index(feature))
                    client.sendTarget(
                            req["id"],
                            type="acknowledge",
                            key="add.map.feature",
                            payload={})

                    return True
            client.sendTarget(
                    req["id"],
                    type="error",
                    key="add.map.feature",
                    payload={
                        "msg": "Feature does not exist at ({0}, {1})"
                             .format(x, y)})
        else:
            client.sendTarget(
                req["id"],
                type="error",
                key="add.map.feature",
                payload={
                    "msg": "User \"{0}\" is on map \"{1}\", however this map could not be found.".format(user["username"], user["current_map"])
            })

        return False
    else:
        client.sendTarget(
            req["id"],
            type="error",
            key="add.map.feature",
            payload={
                "msg": "User with id \"{0}\" has not been registered.".format(req["id"])
        })
        return False


#
# Fog Of War Operations
#

def getMapFow(client, req):
    user = _getUserInfo(id=req["id"])
    if not user:
        client.sendTarget(
            req["id"],
            type="error",
            key="get.map.fow",
            payload={
                "msg": "User with id \"{0}\" has not been registered.".format(req["id"])
        })
        return False

    if user["current_map"] not in magic.game_data["maps"]:
        client.sendTarget(
            req["id"],
            type="error",
            key="get.map.fow",
            payload={
                "msg": "User \"{0}\" is on map \"{1}\", however this map could not be found.".format(user["username"], user["current_map"])
        })
        return False

    fow = magic.game_data["maps"][user["current_map"]]["fow"]
    client.sendTarget(req["id"], key="get.map.fow", payload={"payload": fow})
    return True

def addMapFow(client, req):
    if "x" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="add.map.fow",
                payload={"msg": "Request details missing \"x\""})
        return False
    x = req["details"]["x"]

    if "y" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="add.map.fow",
                payload={"msg": "Request details missing \"y\""})
        return False
    y = req["details"]["y"]

    if not user:
        client.sendTarget(
            req["id"],
            type="error",
            key="remove.map.fow",
            payload={
                "msg": "User with id \"{0}\" has not been registered.".format(req["id"])
        })
        return False


    if user["current_map"] not in magic.game_data["maps"]:
        client.sendTarget(
            req["id"],
            type="error",
            key="remove.map.fow",
            payload={
                "msg": "User \"{0}\" is on map \"{1}\", however this map could not be found.".format(user["username"], user["current_map"])
        })
        return False

    magic.game_data["maps"][user["current_map"]]["fow"][x][y] = True
    client.sendTarget(
            req["id"],
            type="acknowledge",
            key="add.map.fow",
            payload={})
    return True

def removeMapFow(client, req):
    if "x" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="remove.map.fow",
                payload={"msg": "Request details missing \"x\""})
        return False
    x = req["details"]["x"]

    if "y" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="remove.map.fow",
                payload={"msg": "Request details missing \"y\""})
        return False
    y = req["details"]["y"]

    if not user:
        client.sendTarget(
            req["id"],
            type="error",
            key="remove.map.fow",
            payload={
                "msg": "User with id \"{0}\" has not been registered.".format(req["id"])
        })
        return False


    if user["current_map"] not in magic.game_data["maps"]:
        client.sendTarget(
            req["id"],
            type="error",
            key="remove.map.fow",
            payload={
                "msg": "User \"{0}\" is on map \"{1}\", however this map could not be found.".format(user["username"], user["current_map"])
        })
        return False

    magic.game_data["maps"][user["current_map"]]["fow"][x][y] = False
    client.sendTarget(
            req["id"],
            type="acknowledge",
            key="remove.map.fow",
            payload={})
    return True

##########################
# Unit Functions         #
##########################

def getMapUnits(client, req):
    user = _getUserInfo(id=req["id"])
    if not user:
        client.sendTarget(
            req["id"],
            type="error",
            key="get.map.units",
            payload={
                "msg": "User with id \"{0}\" has not been registered.".format(req["id"])
        })
        return False

    if user["current_map"] not in magic.game_data["maps"]:
        client.sendTarget(
            req["id"],
            type="error",
            key="get.map.units",
            payload={
                "msg": "User \"{0}\" is on map \"{1}\", however this map could not be found.".format(user["username"], user["current_map"])
        })

        return False

    units = magic.game_data["maps"][user["current_map"]]["units"]
    client.sendTarget(req["id"], key="get.map.units", payload={"payload": units})
    return True


def addMapUnit(client, req):
    if "x" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="add.map.unit",
                payload={"msg": "Request details missing \"x\""})
        return False
    x = req["details"]["x"]

    if "y" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="add.map.unit",
                payload={"msg": "Request details missing \"y\""})
        return False
    y = req["details"]["y"]

    if "name" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="add.map.unit",
                payload={"msg": "Request details missing \"name\""})
        return False
    name = req["details"]["name"]

    if "max_health" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="add.map.unit",
                payload={"msg": "Request details missing \"max_health\""})
        return False
    max_health = req["details"]["max_health"]

    if "current_health" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="add.map.unit",
                payload={"msg": "Request details missing \"current_health\""})
        return False
    current_health = req["details"]["current_health"]

    if "controller" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="add.map.unit",
                payload={"msg": "Request details missing \"controller\""})
        return False
    controller = req["details"]["controller"]

    if "type" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="add.map.unit",
                payload={"msg": "Request details missing \"type\""})
        return False
    type = req["details"]["type"]

    if "id" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="add.map.unit",
                payload={"msg": "Request details missing \"id\""})
        return False
    type = req["details"]["id"]

    user = _getUserInfo(id=req["id"])
    if not user:
        client.sendTarget(
            req["id"],
            type="error",
            key="add.map.unit",
            payload={
                "msg": "User with id \"{0}\" has not been registered.".format(req["id"])
        })
        return False

    if user["current_map"] not in magic.game_data["maps"]:
        client.sendTarget(
            req["id"],
            type="error",
            key="add.map.unit",
            payload={
                "msg": "User \"{0}\" is on map \"{1}\", however this map could not be found.".format(user["username"], user["current_map"])
        })

        return False

    units = magic.game_data[user["current_map"]]["units"]
    units.append({
        "x": x,
        "y": y,
        "name": name,
        "max_health": max_health,
        "current_health": current_health,
        "controller": controller,
        "type": type,
        "id": id
    })

    client.sendTarget(
            req["id"],
            type="acknowledge",
            key="add.map.unit",
            payload={})
    return True

def modifyMapUnit(client, req):
    if "x" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="modify.map.unit",
                payload={"msg": "Request details missing \"x\""})
        return False
    x = req["details"]["x"]

    if "y" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="modify.map.unit",
                payload={"msg": "Request details missing \"y\""})
        return False
    y = req["details"]["y"]

    if "name" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="modify.map.unit",
                payload={"msg": "Request details missing \"name\""})
        return False
    name = req["details"]["name"]

    if "max_health" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="modify.map.unit",
                payload={"msg": "Request details missing \"max_health\""})
        return False
    max_health = req["details"]["max_health"]

    if "current_health" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="modify.map.unit",
                payload={"msg": "Request details missing \"current_health\""})
        return False
    current_health = req["details"]["current_health"]

    if "controller" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="modify.map.unit",
                payload={"msg": "Request details missing \"controller\""})
        return False
    controller = req["details"]["controller"]

    if "type" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="modify.map.unit",
                payload={"msg": "Request details missing \"type\""})
        return False
    type = req["details"]["type"]

    if "id" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="modify.map.unit",
                payload={"msg": "Request details missing \"id\""})
        return False
    id = req["details"]["type"]

    user = _getUserInfo(id=req["id"])
    if not user:
        client.sendTarget(
            req["id"],
            type="error",
            key="modify.map.unit",
            payload={
                "msg": "User with id \"{0}\" has not been registered.".format(req["id"])
        })
        return False

    if user["current_map"] not in magic.game_data["maps"]:
        client.sendTarget(
            req["id"],
            type="error",
            key="modify.map.unit",
            payload={
                "msg": "User \"{0}\" is on map \"{1}\", however this map could not be found.".format(user["username"], user["current_map"])
        })

        return False

    units = magic.game_data["maps"][user["current_map"]]["units"]
    for unit in units:
        if unit["id"] == id:
            unit["x"] = x
            unit["y"] = y
            unit["name"] = name
            unit["max_health"] = max_health
            unit["current_health"] = current_health
            unit["controller"] = controller
            unit["type"] = type

            client.sendTarget(
                    req["id"],
                    type="acknowledge",
                    key="modify.map.unit",
                    payload={})
        return True

    client.sendTarget(
        req["id"],
        type="error",
        key="modify.map.unit",
        payload={
            "msg": "Note with id \"{0}\" on map \"{1}\".".format(id, user["current_map"])
    })
    return False


def removeMapUnit(client, req):

    if "id" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="remove.map.unit",
                payload={"msg": "Request details missing \"id\""})
        return False
    id = req["details"]["id"]

    user = _getUserInfo(id=req["id"])
    if not user:
        client.sendTarget(
            req["id"],
            type="error",
            key="remove.map.unit",
            payload={
                "msg": "User with id \"{0}\" has not been registered.".format(req["id"])
        })
        return False

    if user["current_map"] not in magic.game_data["maps"]:
        client.sendTarget(
            req["id"],
            type="error",
            key="remove.map.unit",
            payload={
                "msg": "User \"{0}\" is on map \"{1}\", however this map could not be found.".format(user["username"], user["current_map"])
        })

        return False

    units = magic.game_data[user["current_map"]]["units"]

    for unit in units:
        if unit["id"] == id:

            units.remove(unit)

            client.sendTarget(
                    req["id"],
                    type="acknowledge",
                    key="remove.map.unit",
                    payload={})
            return True

    client.sendTarget(
        req["id"],
        type="error",
        key="remove.map.unit",
        payload={
            "msg": "Unit with id \"{0}\" not found on map \"{1}\".".format(id, user["current_map"])
    })
    return False

##########################
# Narrative Functions    #
##########################

def addNarrative(client, req):
    if "name" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="add.narrative",
                payload={"msg": "Request details missing \"name\""})
        return False
    name = req["details"]["name"]

    if "chapter_no" not in req["details"]:
        maximum = max([ el["chapter_no"] for el in magic.game_data["story"]])
        chapter_no = maximum + 1
    else:
        chapter_no = req["details"]["chapter_no"]

    text = req["details"]["text"] if "text" in req["details"] else None

    magic.game_data["story"].append({
        "name": name,
        "chapter_no": chapter_no,
        "text": text
    })

    client.sendTarget(
            req["id"],
            type="acknowledge",
            key="add.narrative",
            payload={})
    return True

def removeNarrative(client, req):
    if "chapter_no" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="add.narrative",
                payload={"msg": "Request details missing \"chapter_no\""})
        return False
    chapter_no = req["details"]["chapter_no"]

    for chapter in magic.game_data["story"]:
        if chapter["chapter_no"] == chapter_no:
            chapters = magic.game_data["story"]
            chapters.remove(chapter)

            higher_no_chapters = [ chapters.index(x) for x in chapters if x["chapter_no"] > chapter_no]

            for x in higher_no_chapters:
                chapters[x]["chapter_no"] -= 1


            client.sendTarget(
                    req["id"],
                    type="acknowledge",
                    key="remove.narrative",
                    payload={})
            return True

    client.sendTarget(
        req["id"],
        type="error",
        key="remove.narrative",
        payload={
            "msg": "Narrative with chapter number \"{0}\" not found .".format(chapter_no)
    })
    return False

def modifyNarrative(client, req):
    if "name" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="modify.narrative",
                payload={"msg": "Request details missing \"name\""})
        return False
    name = req["details"]["name"]

    if "chapter_no" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="modify.narrative",
                payload={"msg": "Request details missing \"chapter_no\""})
        return False
    chapter_no = req["details"]["chapter_no"]

    new_chapter_no = req["details"]["new_chapter_no"] if "new_chapter_no" in req["details"] else None

    if "text" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="modify.narrative",
                payload={"msg": "Request details missing \"text\""})
        return False
    text = req["details"]["text"]

    for chapter in magic.game_data["story"]:
        if chapter["chapter_no"] == chapter_no:

            if new_chapter_no:
                chapter["chapter_no"] = new_chapter_no

            chapter["name"] = name
            chapter["text"] = text

            client.sendTarget(
                    req["id"],
                    type="acknowledge",
                    key="modify.narrative",
                    payload={})
            return True

    client.sendTarget(
        req["id"],
        type="error",
        key="modify.narrative",
        payload={
            "msg": "Narrative with chapter number \"{0}\" not found .".format(chapter_no)
    })
    return False

def getNarrative(client, req):
    if "chapter_no" not in req["details"]:
        client.sendTarget(
                req["id"],
                type="error",
                key="get.narrative",
                payload={"msg": "Request details missing \"chapter_no\""})
        return False
    chapter_no= req["details"]["chapter_no"]

    chapters = sorted(magic.game_data["story"], key=lambda x: x["chapter_no"])
    for chapter in chapters:
        if chapter["chapter_no"] == chapter_no:
            client.sendTarget(
                    req["id"],
                    key="get.narrative", payload={"payload": chapter})
            return True

    client.sendTarget(
        req["id"],
        type="error",
        key="get.narrative",
        payload={
            "msg": "Narrative with chapter number \"{0}\" not found .".format(chapter_no)
        })
    return False



def listNarratives(client, req):
    chapter_names = []

    chapters = sorted(magic.game_data["story"], key=lambda x: x["chapter_no"])

    for chapter in chapters:
        chapter_names.append(chapter["name"])

    client.sendTarget(
            req["id"],
            key="list.narratives", payload={"payload": chapter_names})
    return True


def exportNarratives(client, req):
    out = ""

    chapters = sorted(magic.game_data["story"], key=lambda x: x["chapter_no"])
    for chapter in chapters:
        out += "Chapter {0}: {1}\n {2}\n\n".format(
                chapter["chapter_no"],
                chapter["name"],
                chapter["text"])

    client.sendTarget(
            req["id"],
            key="export.narrative", payload={"payload": chapters})

    return True




##########################
# Save Data Function     #
##########################
def save(client, req):
    print("Saving Data...")
    magic.save()
    print("Data Saved.")
    client.sendTarget(
            req["id"],
            type="acknowledge",
            key="save",
            payload={})


##########################
# Util Functions         #
##########################

def _getUserInfo(id=None, username=None):
    if id is not None:
        for user in magic.users:
            if user["client_id"] == id:
                return user
    elif username is not None:
        for user in magic.users:
            if user["username"] == username:
                return user
    return None


##########################
# Handlers               #
##########################

common_handlers = {
    "get.map": [getMap],

    "register.user": [registerUser],

    "get.chat": [getChat],
}

gm_handlers = {

    "get.users": [getUsers],
    "move.user": [moveUser],

    "add.chat.message": [addChatMessage],
    "clear.chat": [clearChat],

    "add.map": [addMap],
    "remove.map": [removeMap],
    "rename.map": [renameMap],
    "list.maps": [listMaps],

    "add.map.note": [addMapNote],
    "remove.map.note": [removeMapNote],
    "modify.map.note": [modifyMapNote],
    "get.map.notes": [getMapNotes],

    "add.map.feature": [addMapFeature],
    "remove.map.feature": [removeMapFeature],

    "add.map.fow": [addMapFow],
    "remove.map.fow": [removeMapFow],
    "get.map.fow": [getMapFow],

    "add.map.unit": [addMapUnit],
    "remove.map.unit": [removeMapUnit],
    "modify.map.unit": [modifyMapUnit],
    "get.map.units": [getMapUnits],

    "add.narrative": [addNarrative],
    "remove.narrative": [removeNarrative],
    "modify.narrative": [modifyNarrative],
    "get.narrative": [getNarrative],
    "list.narratives": [listNarratives],
    "export.narratives": [exportNarratives],

    "save": [save]
}
