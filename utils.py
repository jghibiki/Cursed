import json

def load(ctx):
    with open(ctx.obj["map_location"], "r") as f:
        return json.load(f)

def save(ctx, map_obj):
    with open(ctx.obj["map_location"], "w") as f:
        json.dump(map_obj, f, indent=4)
