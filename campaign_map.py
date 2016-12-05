import curses
import click
from utils import save, load
import locale

locale.setlocale(locale.LC_ALL, '')



@click.group("map")
@click.pass_context
def campaign_map(ctx):
    pass

@click.command("add")
@click.option("--max-x", default=100, type=int)
@click.option("--max-y", default=100, type=int)
@click.argument("map_name")
@click.pass_context
def add_map(ctx, max_x, max_y, map_name):
    campaign_obj = load(ctx)


    campaign_obj["maps"][map_name] = {
        "max_x": max_x,
        "max_y": max_y,
        "features": [],
        "fow": [ [ False for y in range(max_y) ] for x in range(max_x) ]
    }

    save(ctx, campaign_obj)

@click.command("rm")
@click.argument("map_name")
@click.pass_context
def remove_map(ctx, map_name):
    campaign_obj = load(ctx)
    del campaign_obj["maps"][map_name]
    save(ctx, campaign_obj)

@click.command("list")
@click.pass_context
def list(ctx):
    campaign_obj = load(ctx)
    intro = "%s" % campaign_obj["title"]
    pad = len(intro)*"="
    print("%s\n%s\n%s\nMaps:" % (pad, intro, pad))
    for cmap in campaign_obj["maps"].keys():
        print("|-> %s" % cmap)


@click.command("edit")
@click.argument("map_name")
@click.pass_context
def edit_map(ctx, map_name):
    launch_map_editor(ctx, map_name)

def launch_map_editor(ctx, map_name, queue=None, client=None):
    curses.wrapper(_edit_map, ctx, map_name, queue, client)

def _edit_map(scr, ctx, map_name, queue, client):
    campaign_obj = load(ctx)

    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)

    from features import init_features
    from features import load_features
    from screen import Screen
    from viewport import Viewport
    from viewer import Viewer
    from editor import Editor
    from gm import GM

    init_features()
    features = load_features(campaign_obj["maps"][map_name])

    viewport = Viewport(features,
            campaign_obj["maps"][map_name]["max_y"],
            campaign_obj["maps"][map_name]["max_x"])
    screen = Screen(scr)
    editor = Editor(
            campaign_obj["maps"][map_name]["max_y"],
            campaign_obj["maps"][map_name]["max_x"])


    def save_map(ctx, cmap, campaign_obj):
        def _save_map_callback(map_object):
            campaign_obj["maps"][cmap]["features"] = map_object
            save(ctx, campaign_obj)
        return _save_map_callback
    gm = GM(save_map(ctx, map_name, campaign_obj))

    viewer = Viewer(scr, map_name)

    viewer.register_submodule(viewport)
    viewer.register_submodule(screen)
    viewer.register_submodule(editor)
    viewer.register_submodule(gm)

    viewer.run()



campaign_map.add_command(add_map)
campaign_map.add_command(remove_map)
campaign_map.add_command(edit_map)
campaign_map.add_command(list)


