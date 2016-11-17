import curses
import click
from utils import save, load
from editor import Editor, Map, init
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
        "features": []
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
    curses.wrapper(_edit_map, ctx, map_name)

def _edit_map(scr, ctx, map_name):
    campaign_obj = load(ctx)

    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)

    init()
    campaign_map = Map(campaign_obj["maps"][map_name])
    editor = Editor(scr, campaign_map, save_map(ctx, map_name, campaign_obj))

    zz = False
    while True:
        ch = scr.getch()
        editor.handle(ch)
        editor.draw()

def save_map(ctx, cmap, campaign_obj):
    def _save_map_callback(map_object):
        campaign_obj["campaign_maps"][cmap] = map_object
        save(ctx, campaign_obj)
    return _save_map_callback


campaign_map.add_command(add_map)
campaign_map.add_command(remove_map)
campaign_map.add_command(edit_map)
campaign_map.add_command(list)


