import curses
import curses.textpad
import curses.ascii
import os
from features import Feature, FeatureType, FeatureSerializer
from interactive import *
import logging

log = logging.getLogger('simple_example')

os.environ.setdefault('ESCDELAY', '25')


class Viewer(InteractiveModule, VisibleModule):

    def __init__(self, screen, map_name):

        self.screen = screen
        self.screen.timeout(500)

        self.map_name = map_name

        self._submodules = []

        self._combo_buffer = ""
        self._initial_draw = True


    def run(self):
       self._draw()
       curses.doupdate()

       while True:
            ch = self.screen.getch()

            changes = False

            for mod in self._submodules:
                if isinstance(mod, ClientModule):
                    changes = mod.update(self)

            if ch is not -1:
                self._handle(ch)
            changes = self._draw() or changes

            if changes:
                curses.doupdate()

                for mod in self._submodules:
                    if isinstance(mod, ServerModule):
                        mod.update(self)


    def _draw(self, force=False):
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

        return changes

    def _handle_combo(self, ch):
            if ch == 27 or ch == curses.ascii.ESC: # escape
                self._combo_buffer = None

                from status_line import StatusLine
                sl = self.get_submodule(StatusLine)
                sl.clear_buff()

            elif ch == curses.KEY_ENTER or ch == 10 or ch == 13:

                if self._combo_buffer[0] == ":":
                    for module in self._submodules:
                        if isinstance(module, InteractiveModule):
                            module._handle_combo(self, self._combo_buffer[1:])

                    if "q" == self._combo_buffer[1]:
                        exit()

                    if (len(self._combo_buffer) > 2 and
                        "h" == self._combo_buffer[0] and
                        " " == self._combo_buffer[1]):
                            self.handle_help(self._combo_buffer[2:])

                # reset buffer
                self._combo_buffer = ""

                from status_line import StatusLine
                sl = self.get_submodule(StatusLine)
                sl.clear_buff()


            elif ch == curses.KEY_BACKSPACE or ch == 127 or ch == 8 or ch == curses.ascii.BS:
                self._combo_buffer = self._combo_buffer[:len(self._combo_buffer)-1]

                from status_line import StatusLine
                sl = self.get_submodule(StatusLine)
                sl.set_buff(self._combo_buffer)

            else:
                self._combo_buffer += chr(ch)

                from status_line import StatusLine
                sl = self.get_submodule(StatusLine)
                sl.set_buff(self._combo_buffer)

                #self.screen.addstr(ViewerConstants.max_y,0, self._combo_buffer)

    def _handle_help(self, buf):
        for mod in self._submodules:
            if isinstance(mod, InteractiveModule):
                mod._handle_help(self, buf)

    def _handle(self, ch):

        if self._combo_buffer:
                self._handle_combo(ch)

        else:
            if ch == ord(":"):
                self._combo_buffer = ":"
                from status_line import StatusLine
                sl = self.get_submodule(StatusLine)
                sl.set_buff(self._combo_buffer)
                #self.screen.addstr(ViewerConstants.max_y, 0, self._combo_buffer)

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


class ViewerConstants:
    min_y = 0
    min_x = 0
    max_y = (curses.LINES - 1)
    max_x = (curses.COLS - 1)

