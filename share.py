from utils import load, save
import click
import queue
import logging
import curses
from app_server import run as start_app_server

log = logging.getLogger('simple_example')


@click.group()
@click.pass_context
def share(ctx):
    pass


@click.group()
@click.pass_context
def server(ctx):
    """
    Tools for starting and running a server.
    """
    pass

@click.command("start")
@click.option("--port", default=8080)
@click.option("--host", default="0.0.0.0")
@click.option("--gm-password", default=None)
@click.option("--password", default=None)
@click.argument("map_name")
@click.pass_context
def start_server(ctx, port, host, map_name, gm_password, password):
    """
    Starts a server
    """
    game_data = load(ctx)
    start_app_server(game_data, port, host,gm_password, password)



#def _start_server(scr, ctx, map_name):
#    log.debug("Starting server")
#    campaign_obj = load(ctx)
#
#    curses.start_color()
#    curses.use_default_colors()
#    for i in range(0, curses.COLORS):
#        curses.init_pair(i + 1, i, -1)
#
#    from features import init_features
#    from features import load_features
#    from screen import Screen
#    from viewport import Viewport
#    from viewer import Viewer
#    from gm import GM
#    from editor import Editor
#    from server import Server
#    from status_line import StatusLine
#
#    init_features()
#    features = load_features(campaign_obj["maps"][map_name])
#
#    viewport = Viewport(features,
#            campaign_obj["maps"][map_name]["max_y"],
#            campaign_obj["maps"][map_name]["max_x"])
#    screen = Screen(scr)
#    editor = Editor(
#            campaign_obj["maps"][map_name]["max_y"],
#            campaign_obj["maps"][map_name]["max_x"])
#    status_line = StatusLine(curses.LINES, curses.COLS)


#    def save_map(ctx, cmap, campaign_obj):
#        def _save_map_callback(map_object):
#            campaign_obj["maps"][cmap]["features"] = map_object
#            save(ctx, campaign_obj)
#        return _save_map_callback
#    gm = GM(save_map(ctx, map_name, campaign_obj))
#
#    server = Server()
#    viewer = Viewer(scr, map_name)
#
#    viewer.register_submodule(viewport)
#    viewer.register_submodule(screen)
#    viewer.register_submodule(editor)
#    viewer.register_submodule(gm)
#    viewer.register_submodule(status_line)
#    viewer.register_submodule(server)
#
#    log.debug("running viewer")
#    viewer.run()

server.add_command(start_server)


@click.group()
@click.pass_context
def client(ctx):
    """
    Tools for connecting to a dmtools server as a player.
    """
    pass

@click.command("join")
@click.option("--host", default="127.0.0.1")
@click.option("--port", default=5489)
@click.argument("password")
@click.pass_context
def client_join(ctx, host, port, password):
    """
    Join a dmtools server.
    """
    curses.wrapper(_client_join, ctx, host, port, password)

def _client_join(scr, ctx, host, port, password):
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)

    from features import init_features
    from features import load_features
    from screen import Screen
    from viewport import Viewport
    from viewer import Viewer
    from pc import PC
    from status_line import StatusLine
    from client import Client

    init_features()

    features = []
    viewport = Viewport(features, 0, 0)
    status_line = StatusLine(curses.LINES, curses.COLS)
    screen = Screen(scr)
    pc = PC()
    client = Client(password)
    viewer = Viewer(scr, "")

    viewer.register_submodule(viewport)
    viewer.register_submodule(screen)
    viewer.register_submodule(pc)
    viewer.register_submodule(status_line)
    viewer.register_submodule(client)

    viewer.run()


client.add_command(client_join)

share.add_command(server)
share.add_command(client)
