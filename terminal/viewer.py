import curses
import curses.textpad
import curses.ascii
import os
from interactive import *
import log
import random
from datetime import datetime

log = log.logger

NUMBERS = [ ord("0"), ord("1"), ord("2"), ord("3"), ord("4"), ord("5"), ord("6"), ord("7"), ord("8"), ord("9") ]
VIM_DIRECTIONS = [ ord("j"), ord("k"), ord("h"), ord("l"), ord("J"), ord("K"), ord("H"), ord("L")]
WSAD_DIRECTIONS = [ ord("w"), ord("s"), ord("a"), ord("d"), ord("W"), ord("S"), ord("A"), ord("D") ]

class Viewer(InteractiveModule, VisibleModule):

    instance = None

    def __init__(self, screen):

        self.screen = screen
        self.screen.timeout(1000)
        self.screen.idcok(False)
        self.screen.idlok(False)

        self._submodules = []

        self._motion_buffer_count = ""
        self._motion_buffer = ""

        self._combo_buffer = ""
        self._initial_draw = True
        self._mind_blown = False

        self.loop = None
        self.client = None
        self.client_connected = False

        curses.curs_set(0)

        Viewer.instance = self


    def run(self):
        self._draw()
        curses.doupdate()

        for mod in self._submodules:
            if isinstance(mod, InitModule):
                mod.update(self)

        while True: # to preserve old behavior where run keeps looping
            self.tick()

    def tick(self):
        if not self.client_connected:
            self.loop.call_soon(self.tick)
            return

        self.client.ping()

        # hacks to fix terminal state
        curses.curs_set(0)

        # get ch
        ch = self.screen.getch()

        self.start = datetime.now()

        changes = False

        log.debug("Calling update on client modules")
        part_start = datetime.now()
        for mod in self._submodules:
            if isinstance(mod, ClientModule):
                changes = mod.update(self)
        log.debug("Elapsed: %s" % (datetime.now() - part_start))

        log.debug("Calling handle")
        part_start = datetime.now()
        if ch is not -1:
            self._handle(ch)
        log.debug("Elapsed %s" % (datetime.now() - part_start))

        log.debug("Calling draw")
        part_start = datetime.now()
        changes = self._draw() or changes
        log.debug("Elapsed %s" % (datetime.now() - part_start))


        if self._mind_blown and changes:

            curses.start_color()
            curses.use_default_colors()
            for i in range(1, curses.COLORS):
                color = random.randint(1, curses.COLORS-1)
                curses.init_pair(i + 1, color, -1)

        # part of an ongoing expiriment to see if this helps with character repeat lag
        curses.flushinp() # get rid of any characters waiting in buffer

        end = datetime.now()
        elapsed = end - self.start

        log.info("Main loop duration: %s" % elapsed)

        if self.loop:
            self.loop.call_soon(self.tick)


    def setLoop(self, loop):
        self.loop = loop

    def setClient(self, client):
        self.client = client

        def client_connected_cb():
            self.client_connected = True

        self.client.register_connect_hook(client_connected_cb)
        self.client.register_connect_hook(self.register_user)

        self.registerHooks()


    def register_user(self):
        log.info("Registering user with server.")
        self.client.send({
            "type": "command",
            "key": "register.user",
            "details": {
                "username": "jghibiki",
                "current_map": "__staging__"
            }
        })

    def registerHooks(self):
        for module in self._submodules:
            if isinstance(module, LiveModule):
                module._register_hooks(self.client)



    def _draw(self, force=False):
        if force: log.debug("viewer._draw forced")
        changes = False
        visible_modules = []
        for module in self._submodules:
            if isinstance(module, VisibleModule):
                visible_modules.append(module)

        if self._initial_draw:
            visible_modules = sorted(visible_modules, key=lambda x: x.initial_draw_priority, reverse=True)
            self._initial_draw = False
        else:
            visible_modules = sorted(visible_modules, key=lambda x: x.draw_priority, reverse=True)

        for module in visible_modules:
            mod_changed = module.draw(self, force=force)
            if mod_changed:
                log.debug("module %s has updated." % module)
                changes = True

        if changes:
                curses.doupdate()
        return changes

    def _handle_combo(self, ch):
            if ch == 27 or ch == curses.ascii.ESC: # escape
                self._combo_buffer = None

                from colon_line import ColonLine
                cl = self.get_submodule(ColonLine)
                cl.clear_buff()

            elif ch == curses.KEY_ENTER or ch == 10 or ch == 13:

                if self._combo_buffer[0] == ":":
                    for module in self._submodules:
                        if isinstance(module, InteractiveModule):
                            module._handle_combo(self, self._combo_buffer[1:])

                    if "q" == self._combo_buffer[1]:
                        exit()

                    elif self._combo_buffer[1:] == "redraw!":
                        self._draw(force=True)

                    elif "save" == self._combo_buffer[1:] or "w" == self._combo_buffer[1:]:
                        from client import Client
                        client = self.get_submodule(Client)
                        log.info("Saving Data")
                        client.make_request("/save")
                        log.info("Saved Data")

                    elif "easter_egg" == self._combo_buffer[1:]:
                        from colon_line import ColonLine
                        cl = self.get_submodule(ColonLine)
                        cl.set_msg("Created by Jordan Goetze! Thanks for using!")

                    elif "super_easter_egg" == self._combo_buffer[1:]:
                        from colon_line import ColonLine
                        cl = self.get_submodule(ColonLine)
                        cl.set_msg("Created by Jordan Goetze! Thanks for using!")
                        import subprocess, os
                        FNULL = open(os.devnull, 'w')
                        try: # lazily handle failure
                            subprocess.call(["espeak", "Created by Jordan Goetze! Thanks for using!"], stdout=FNULL, stderr=subprocess.STDOUT)
                        except:
                            pass

                    elif "mind_blown" == self._combo_buffer[1:]:
                        self._mind_blown = True

                    elif ( len(self._combo_buffer) > 2 and
                           "h" == self._combo_buffer[1:] or
                           "help" == self._combo_buffer[1:] ):
                        self._handle_help(self._combo_buffer[2:])

                # reset buffer
                self._combo_buffer = ""

                from colon_line import ColonLine
                cl = self.get_submodule(ColonLine)
                cl.clear_buff()


            elif ch == curses.KEY_BACKSPACE or ch == 127 or ch == 8 or ch == curses.ascii.BS:
                self._combo_buffer = self._combo_buffer[:len(self._combo_buffer)-1]

                from colon_line import ColonLine
                cl = self.get_submodule(ColonLine)
                cl.set_buff(self._combo_buffer)

            else:
                self._combo_buffer += chr(ch)

                from colon_line import ColonLine
                cl = self.get_submodule(ColonLine)
                cl.set_buff(self._combo_buffer)

                #self.screen.addstr(ViewerConstants.max_y,0, self._combo_buffer)

    def _handle_help(self, buf):
        for mod in self._submodules:
            if isinstance(mod, InteractiveModule):
                log.error(mod)
                mod._handle_help(self, buf)

    def _handle(self, ch):

        if self._combo_buffer:
                self._handle_combo(ch)

        elif self._motion_buffer_count != "":

            from state import State
            state = self.get_submodule(State)
            # check direction scheme
            valid_direction = False
            if state.get_state("direction_scheme") == "wsad":
                if ch in WSAD_DIRECTIONS:
                    valid_direction = True
            elif state.get_state("direction_scheme") == "vim":
                if ch in VIM_DIRECTIONS:
                    valid_direction = True


            if ch == 27 or ch == curses.ascii.ESC: # escape
                self._motion_buffer_count = ""
                self._motion_buffer = ""
            elif ch in NUMBERS:
                self._motion_buffer_count += chr(ch)

            elif self._motion_buffer == "" and not valid_direction:
                self._motion_buffer = ch
            else:

                if valid_direction:
                    valid_count = True
                    try:
                        count = int(self._motion_buffer_count)
                    except:
                        log.warn("bad motion buffer count %s" % self._motion_buffer_count)
                        valid_count = False

                    direction = None
                    if self._motion_buffer != "":
                        char = self._motion_buffer
                        direction = ch
                    else:
                        char = ch

                    # clear these so we don't enter a motion loop
                    self._motion_buffer = ''
                    self._motion_buffer_count = ""
                    if valid_count:
                        for x in range(0, count): #send key then direction
                            self._handle(char)
                            if direction:
                                self._handle(direction)

        else:
            if ch == ord(":"):
                self._combo_buffer = ":"
                from colon_line import ColonLine
                cl = self.get_submodule(ColonLine)
                cl.set_buff(self._combo_buffer)
                #self.screen.addstr(ViewerConstants.max_y, 0, self._combo_buffer)

            elif ch in NUMBERS:
                self._motion_buffer_count += chr(ch)

            else:
                for mod in self._submodules:
                    if isinstance(mod, InteractiveModule):
                        mod._handle(self, ch)

    def register_submodule(self, submodule):
        self._submodules.append(submodule)

    def deregister_submodule(self, submodule):
        self._submodules.remove(submodule)

    def get_submodule(self, module_type):
        for submodule in self._submodules:
            if isinstance(submodule, module_type):
                return submodule

    def apply_to_submodules(self, module_type, callback):
        for submodule in self._submodules:
            if isinstance(submodule, module_type):
                callback(submodule)

    def get_submodules(self, module_type):
        modules = []
        for submodule in self._submodules:
            if isinstance(submodule, module_type):
                modules.append(submodule)
        return modules


class ViewerConstants:
    min_y = 0
    min_x = 0
    max_y = (curses.LINES - 1)
    max_x = (curses.COLS - 1)

