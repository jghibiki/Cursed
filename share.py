from utils import load, save
import click
import queue
import logging
import curses
import requests
import json
import os
from app_server import run as start_app_server

log = logging.getLogger('simple_example')


@click.group()
@click.pass_context
def share(ctx):
    pass


@click.command()
@click.option("--port", default=8080)
@click.option("--host", default="0.0.0.0")
@click.option("--gm-password", default=None)
@click.option("--password", default=None)
@click.argument("map_name")
@click.pass_context
def server(ctx, port, host, map_name, gm_password, password):
    """
    Starts a server
    """
    game_data = load(ctx)
    def save_callback(data):
        save(ctx, data)
    start_app_server(game_data, port, host, gm_password, password, map_name, save_callback)


@click.command("gm")
@click.option("--host", default="127.0.0.1")
@click.option("--port", default=8080)
@click.option("--username", default="")
@click.option("--wsad", is_flag=True, default=False)
@click.argument("password")
@click.argument("map_name")
@click.pass_context
def gm(ctx, host, port, username, wsad, password, map_name):
    """
    Join a dmtools server.
    """
    os.environ.setdefault('ESCDELAY', '5')
    curses.wrapper(_gm_join,ctx, host, port, username, wsad, password, map_name)

def _gm_join(scr, ctx, host, port, username, wsad, password, map_name):
    log.debug("Starting gm client")

    # initialize curses colors
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)

    from features import init_features
    from features import load_features
    from screen import Screen
    from viewport import Viewport
    from viewer import Viewer
    from text_box import TextBox
    from gm import GM
    from editor import Editor
    from colon_line import ColonLine
    from client import Client
    from narrative import Narrative
    from command_window import CommandWindow
    from state import State
    from chat import Chat
    from status_line import StatusLine
    from roll import Roll
    from map import Map

    init_features()
    features = []

    # instanciating modules
    roll = Roll()
    viewport = Viewport(features, 0, 0)
    screen = Screen(scr)
    editor = Editor(0, 0)
    colon_line = ColonLine(curses.LINES, curses.COLS)
    client = Client(password, map_name, host=host, port=port)
    gm = GM()
    cw = CommandWindow()
    narrative = Narrative()
    tb = TextBox()
    state = State()
    chat = Chat()
    sl = StatusLine(curses.LINES, curses.COLS)
    viewer = Viewer(scr, map_name)
    map = Map()

    state.set_state("role", "gm")
    state.set_state("direction_scheme", "wsad" if wsad else "vim")
    state.set_state("username", username)

    # registering modules with viewer module
    viewer.register_submodule(map)
    viewer.register_submodule(roll)
    viewer.register_submodule(state)
    viewer.register_submodule(sl)
    viewer.register_submodule(chat)
    viewer.register_submodule(tb)
    viewer.register_submodule(viewport)
    viewer.register_submodule(screen)
    viewer.register_submodule(editor)
    viewer.register_submodule(gm)
    viewer.register_submodule(cw)
    viewer.register_submodule(narrative)
    viewer.register_submodule(colon_line)
    viewer.register_submodule(client)

    # set current map
    url = "http://%s:%s/map" % (host, port)
    r = requests.post(
            url,
            data=json.dumps({"map_name": map_name}),
            auth=("user", password),
            headers={'content-type': 'application/json'})
    if r.status_code is not 200:
        log.error("Failed to set map name. %s %s %s" % (url, map_name, r.text))
        exit()

    log.debug("running viewer")
    viewer.run()




@click.command("pc")
@click.option("--host", default="127.0.0.1")
@click.option("--port", default=8080)
@click.argument("password")
@click.pass_context
def pc(ctx, host, port, password):
    """
    Join a dmtools server.
    """
    curses.wrapper(_pc_join, ctx, host, port, password)

def _pc_join(scr, ctx, host, port, password):
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
    from colon_line import ColonLine
    from client import Client
    from command_window import CommandWindow
    from state import State
    from chat import Chat
    from status_line import StatusLine
    from colon_line import ColonLine
    from text_box import TextBox
    from roll import Roll
    from map import Map

    init_features()

    features = []
    roll = Roll()
    viewport = Viewport(features, 0, 0)
    colon_line = ColonLine(curses.LINES, curses.COLS)
    screen = Screen(scr)
    pc = PC()
    client = Client(password, host=host, port=port)
    viewer = Viewer(scr, "")
    state = State()
    chat = Chat()
    sl = StatusLine(curses.LINES, curses.COLS)
    tb = TextBox()
    command_window = CommandWindow()
    map = Map()

    state.set_state("role", "pc")

    viewer.register_submodule(map)
    viewer.register_submodule(roll)
    viewer.register_submodule(command_window)
    viewer.register_submodule(viewport)
    viewer.register_submodule(screen)
    viewer.register_submodule(pc)
    viewer.register_submodule(colon_line)
    viewer.register_submodule(client)
    viewer.register_submodule(state)
    viewer.register_submodule(sl)
    viewer.register_submodule(chat)
    viewer.register_submodule(tb)

    viewer.run()



share.add_command(server)
share.add_command(pc)
share.add_command(gm)
