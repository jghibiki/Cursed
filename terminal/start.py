import curses
import log
import os
import broadcast_client

log = log.logger

def entry_point(scr):

    curses.start_color()
    curses.use_default_colors()
    curses.init_color(0, 0, 0, 0)

    username = "jghibiki"
    password = "1111"
    host = "localhost"
    port = 9000
    role = "gm"
    wsad = False

    import config
    from parser import load_config
    load_config()


# load viewer
    from viewer import Viewer
    viewer = Viewer(scr)

# load submodules
    from screen import Screen
    screen = Screen(scr)
    viewer.register_submodule(screen)

    from viewport import Viewport
    viewport = Viewport()
    viewer.register_submodule(viewport)

    from text_box import TextBox
    tb = TextBox()
    viewer.register_submodule(tb)

    from colon_line import ColonLine
    colon_line = ColonLine()
    viewer.register_submodule(colon_line)

    from client import Client
    client = Client(password, host=host, port=port)
    viewer.register_submodule(client)

    from command_window import CommandWindow
    cw = CommandWindow()
    viewer.register_submodule(cw)

    from state import State
    state = State()
    state.set_state("role", role)
    state.set_state("direction_scheme", "wsad" if wsad else "vim")
    state.set_state("username", username)
    viewer.register_submodule(state)

    from chat import Chat
    chat = Chat()
    viewer.register_submodule(chat)

    from status_line import StatusLine
    sl = StatusLine()
    viewer.register_submodule(sl)

    from roll import Roll
    roll = Roll()
    viewer.register_submodule(roll)

    from map import Map
    map = Map()
    viewer.register_submodule(map)

    from users import Users
    users = Users()
    viewer.register_submodule(users)

    from initiative_tracker import InitiativeTracker
    initiative_tracker = InitiativeTracker()
    viewer.register_submodule(initiative_tracker)

    if role == "gm":
        from gm import GM
        gm = GM()
        viewer.register_submodule(gm)

        from narrative import Narrative
        narrative = Narrative()
        viewer.register_submodule(narrative)

    elif role == "pc":
        from pc import PC
        pc = PC()
        viewer.register_submodule(pc)

    log.debug("running viewer")
    client.init(viewer)
    #viewer.run()

    broadcast_client.start_client("127.0.0.1", 9000, viewer)

os.environ.setdefault('ESCDELAY', '5')
curses.wrapper(entry_point)
