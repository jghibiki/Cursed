import json

def load(ctx):
    with open(ctx.obj["data_location"], "r") as f:
        return json.load(f)

def save(ctx, map_obj):
    with open(ctx.obj["data_location"], "w") as f:
        json.dump(map_obj, f, indent=4)


def get_submodules(classes=[]):
    import viewer
    viewer = viewer.Viewer.instance
    instances = [viewer]

    if type(classes) == list:
        for cls in classes:
            instances.append(viewer.get_submodule(cls))
    else:
        instances.append(viewer.get_submodule(classes))

    return viewer if len(instances) == 1 else instances
