import curses
import click
from utils import save, load
from editor import Editor, Map, init
import locale

locale.setlocale(locale.LC_ALL, '')



@click.group()

@click.pass_context
def region(ctx):
    pass

@click.command("add")
@click.option("--max-x", default=100, type=int)
@click.option("--max-y", default=100, type=int)
@click.argument("region_name")
@click.pass_context
def add_region(ctx, max_x, max_y, region_name):
    campaign_obj = load(ctx)


    campaign_obj["regions"][region_name] = {
        "max_x": max_x,
        "max_y": max_y,
        "features": []
    }

    save(ctx, campaign_obj)

@click.command("rm")
@click.argument("region_name")
@click.pass_context
def remove_region(ctx, region_name):
    campaign_obj = load(ctx)
    del campaign_obj["regions"][region_name]
    save(ctx, campaign_obj)

@click.command("list")
@click.pass_context
def list(ctx):
    campaign_obj = load(ctx)
    intro = "%s" % campaign_obj["title"]
    pad = len(intro)*"="
    print("%s\n%s\n%s\nRegions:" % (pad, intro, pad))
    for region in campaign_obj["regions"].keys():
        print("|-> %s" % region)


@click.command("edit")
@click.argument("region_name")
@click.pass_context
def edit_region(ctx, region_name):
    curses.wrapper(_edit_region, ctx, region_name)

def _edit_region(scr, ctx, region_name):
    campaign_obj = load(ctx)

    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)

    init()
    map = Map(campaign_obj["regions"][region_name])
    editor = Editor(scr, map, save_region(ctx, region_name, campaign_obj))

    zz = False
    while True:
        ch = scr.getch()
        editor.handle(ch)
        editor.draw()

def save_region(ctx, region, campaign_obj):
    def _save_region_callback(region_object):
        campaign_obj["regions"][region] = region_object
        save(ctx, campaign_obj)
    return _save_region_callback


region.add_command(add_region)
region.add_command(remove_region)
region.add_command(edit_region)
region.add_command(list)


