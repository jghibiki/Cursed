import curses
import curses.textpad
import os
from features import Feature, FeatureType, FeatureSerializer
from interactive import *

os.environ.setdefault('ESCDELAY', '25')


class Viewer(InteractiveModule, VisibleModule):

    def __init__(self, screen, map_name):

        self.screen = screen
        self.screen.timeout(5000)

        self.map_name = map_name

        self._submodules = []

        self._combo_buffer = ""


    def run(self):
       self._draw()
       curses.doupdate()

       while True:
            ch = self.screen.getch()

            for mod in self._submodules:
                if isinstance(mod, ClientModule):
                    mod.connect()
                    mod.update(self)
                    mod.disconnect()

            if ch is not -1:
                self._handle(ch)
            changes = self._draw()

            if changes:
                curses.doupdate()

                for mod in self._submodules:
                    if isinstance(mod, ServerModule):
                        mod.update(self)


    def _draw(self):
        changes = False
        visible_modules = []
        for module in self._submodules:
            if isinstance(module, VisibleModule):
                visible_modules.append(module)

        visible_modules = sorted(visible_modules, key=lambda x: x.draw_priority, reverse=True)
        for module in visible_modules:
            mod_changed = module.draw(self)
            if mod_changed: changes = True

        return changes

    def _handle_combo(self, ch):
            if ch == 27: # escape
                self._combo_buffer = ""
                self.dirty = True

            if ch == curses.KEY_ENTER or ch == 10 or ch == 13:

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
                self.dirty = True
            else:
                self._combo_buffer += chr(ch)
                self.screen.addstr(ViewerConstants.max_y,0, self._combo_buffer)

    def _handle_help(self, buf):
        for mod in self._submodules:
            if isinstance(mod, InteractiveModule):
                mod._handle_help(self, buf)

    def _handle(self, ch):

        if self._combo_buffer:
                self._handle_combo(ch)

        else:
            if ch == ord(":"):
                self._combo_buffer += ":"
                self.screen.addstr(ViewerConstants.max_y, 0, self._combo_buffer)

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

