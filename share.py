from utils import load
import curses
import click
import queue
import logging

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
@click.argument("map_name")
@click.pass_context
def start_server(ctx, map_name):
    """
    Starts a server, controlled by the GM.
    """
    curses.wrapper(_start_server, ctx, map_name)

def _start_server(scr, ctx, map_name):
    log.debug("Starting server")
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
    from gm import GM
    from server import Server

    init_features()
    features = load_features(campaign_obj["maps"][map_name])

    viewport = Viewport(features,
            campaign_obj["maps"][map_name]["max_y"],
            campaign_obj["maps"][map_name]["max_x"])
    screen = Screen(scr)
    gm = GM()
    server = Server()
    viewer = Viewer(scr, map_name)

    viewer.register_submodule(viewport)
    viewer.register_submodule(screen)
    viewer.register_submodule(gm)
    viewer.register_submodule(server)

    log.debug("running viewer")
    viewer.run()

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
@click.pass_context
def client_join(ctx, host, port):
    """
    Join a dmtools server.
    """
    curses.wrapper(_client_join, ctx, host, port)

def _client_join(scr, ctx, host, port):
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)

    from features import init_features
    from features import load_features
    from screen import Screen
    from viewport import Viewport
    from viewer import Viewer
    from gm import GM
    from client import Client

    init_features()

    features = []
    viewport = Viewport(features, 0, 0)
    screen = Screen(scr)
    gm = GM()
    client = Client()
    viewer = Viewer(scr, "")

    viewer.register_submodule(viewport)
    viewer.register_submodule(screen)
    viewer.register_submodule(gm)
    viewer.register_submodule(client)

    viewer.run()


client.add_command(client_join)

share.add_command(server)
share.add_command(client)
