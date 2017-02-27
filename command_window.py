from interactive import VisibleModule, InteractiveModule, TextDisplayModule
from viewer import ViewerConstants
from viewport import Viewport
from client import Client
from state import State
import colors
import json
import logging
import curses
import math
import os
import subprocess
import tempfile

import keybindings
import features

log = logging.getLogger('simple_example')

class CommandMode:
    default = 0
    build = 1
    fow = 2
    units = 3
    unit_move = 4
    box_select = 5


class CommandWindow(VisibleModule, InteractiveModule):
    def __init__(self):
        self.initial_draw_priority = -1
        self.draw_priority = 9

        self.x = math.floor(ViewerConstants.max_x/2) + math.floor(ViewerConstants.max_x/3)+1
        self.y = 0
        self.h = ViewerConstants.max_y-2
        self.w = ViewerConstants.max_x - math.floor(ViewerConstants.max_x/2) - math.floor(ViewerConstants.max_x/3) #TODO: fix sketchy math

        self._screen = curses.newwin(self.h, self.w, self.y, self.x)

        self._mode = CommandMode.default

        self._box_refferer = -1
        self._box_xy = None
        self._box_xy2 = None
        self._box_returning = False
        self._box = False

        self._count = ""

        self._dirty = True

    def draw(self, viewer, force=False):
        if self._dirty or force:
            if force: log.debug("command_window.draw forced")

            self._screen.clear()

            state = viewer.get_submodule(State)
            self._screen.attrset(colors.get("Gold"))
            if state.get_state("easter_egg") is not None:
                self._screen.border(
                        curses.ACS_VLINE,
                        curses.ACS_VLINE,
                        curses.ACS_HLINE,
                        curses.ACS_HLINE,
                        curses.ACS_DIAMOND,
                        curses.ACS_DIAMOND,
                        curses.ACS_DIAMOND,
                        curses.ACS_DIAMOND
                )
            else:
                self._screen.border(
                        curses.ACS_BOARD,
                        curses.ACS_BOARD,
                        curses.ACS_BOARD,
                        curses.ACS_BOARD,
                        curses.ACS_BOARD,
                        curses.ACS_BOARD,
                        curses.ACS_BOARD,
                        curses.ACS_BOARD
                )
            self._screen.attroff(colors.get("Gold"))

            state = viewer.get_submodule(State)
            role = state.get_state("role")

            if self._mode is CommandMode.default:
                if role == "pc":
                    self._draw_pc_default_screen()
                elif role == "gm":
                    self._draw_gm_default_screen()
            if self._mode is CommandMode.build: self._draw_build_screen()
            if self._mode is CommandMode.fow: self._draw_fow_screen()
            if self._mode is CommandMode.units: self._draw_units_screen(viewer)
            if self._mode is CommandMode.unit_move: self._draw_unit_move_screen(viewer)
            if self._mode is CommandMode.box_select: self._draw_box_select_screen()

            self._screen.noutrefresh()
            self._dirty = False
            return True
        return False

    def _handle(self, viewer, ch):
        state = viewer.get_submodule(State)
        role = state.get_state("role")
        if self._mode is CommandMode.default:
            if ch == ord("b") and role == "gm":
                self._mode = CommandMode.build
                self._dirty = True

            elif ch == ord("c"):
                from chat import Chat
                chat = viewer.get_submodule(Chat)
                viewer.apply_to_submodules(TextDisplayModule, lambda x: x._hide(viewer))
                chat._show(viewer)

            elif ch == ord("n") and role == "gm":
                from narrative import Narrative
                narrative = viewer.get_submodule(Narrative)
                viewer.apply_to_submodules(TextDisplayModule, lambda x: x._hide(viewer))
                narrative._show(viewer)

            elif ch == ord("f") and role == "gm":
                vp = viewer.get_submodule(Viewport)
                current = state.get_state("fow")
                if current == "on":
                    state.set_state("fow", "off")
                else:
                    state.set_state("fow", "on")
                vp._dirty = True
                viewer._draw(force=True)

            elif ch == ord("F") and role == "gm":
                self._mode = CommandMode.fow
                self._dirty = True

            elif ch == ord("u"):
                state = viewer.get_submodule(State)
                state.set_state("ignore_direction_keys", "on")
                self._mode = CommandMode.units
                self._dirty = True

            elif ch == ord("m"):
                from map import Map
                m = viewer.get_submodule(Map)
                m._show(viewer)

        elif self._mode is CommandMode.build: #gm only
            if ch == 27 or ch == curses.ascii.ESC: # escape
                if self._box:
                    vp = viewer.get_submodule(Viewport)
                    vp.box_xy = None
                    vp._dirty = True

                    self._dirty = True
                    self._box = False
                else:
                    self._mode = CommandMode.default
                    self._dirty = True

            for binding in keybindings.build:
                if ch == ord(binding["key"]):

                    vp = viewer.get_submodule(Viewport)
                    c = viewer.get_submodule(Client)

                    if self._box:
                        x_min = min(self._box_xy[0], self._box_xy2[0])
                        x_max = max(self._box_xy[0], self._box_xy2[0]) + 1

                        y_min = min(self._box_xy[1], self._box_xy2[1])
                        y_max = max(self._box_xy[1], self._box_xy2[1]) + 1

                        payload = [ features.new_feature(binding["type"], x, y) for x in range(x_min, x_max) for y in range(y_min, y_max) ]
                        c.make_request("/map/bulk/add", payload={"features": payload})
                        self._box = False
                        vp.box_xy = None
                        vp._dirty = True


                    else:

                        feature = features.new_feature(binding["type"], vp.cursor_x, vp.cursor_y)
                        c.make_request("/map/add", payload=feature)


            if ch == ord("x"):
                vp = viewer.get_submodule(Viewport)
                c = viewer.get_submodule(Client)
                if self._box:
                    x_min = min(self._box_xy[0], self._box_xy2[0])
                    x_max = max(self._box_xy[0], self._box_xy2[0]) + 1

                    y_min = min(self._box_xy[1], self._box_xy2[1])
                    y_max = max(self._box_xy[1], self._box_xy2[1]) + 1

                    payload = [ {"x": x, "y": y } for x in range(x_min, x_max) for y in range(y_min, y_max) ]
                    c.make_request("/map/bulk/rm", payload={"features": payload})

                    self._box = False
                    vp.box_xy = None
                    vp._dirty = True

                else:
                    c.make_request("/map/rm", payload={
                        "x": vp.cursor_x,
                        "y": vp.cursor_y
                    })

            elif ch == ord(" "):
                vp = viewer.get_submodule(Viewport)
                self._box_xy = ( vp.cursor_x, vp.cursor_y )
                vp.box_xy = self._box_xy
                vp._dirty = True
                self._box_referer = self._mode
                self._mode = CommandMode.box_select
                self._dirty = True


        elif self._mode is CommandMode.box_select:
            if ch == ord(" "):
                vp = viewer.get_submodule(Viewport)
                self._box_xy2 = ( vp.cursor_x, vp.cursor_y)
                self._box = True
                self._mode = self._box_referer
                self._dirty = True

            elif ch == 27 or ch == curses.ascii.ESC:
                self._box_returning = True
                self._box = False
                self._mode = self._box_referer
                self._box_referer = -1
                self._dirty = True

                vp = viewer.get_submodule(Viewport)
                vp.box_xy = None
                vp._dirty = True


        elif self._mode is CommandMode.units:
            if ch == 27 or ch == curses.ascii.ESC:
                self._mode = CommandMode.default
                state = viewer.get_submodule(State)
                state.set_state("ignore_direction_keys", "off")
                self._dirty = True

            elif ch == ord("a"):

                unit_text = """
# Name: Name of the unit
# Max Health: the unit's maximum health
# Current Health: the unit's current health, must be less than or equal to max health
# Controller: The owner of the unit. Only the owner and the gm can move the unit.
# Type: The type of the unit, must be one of the following. If not set defaults to neutral.
#   - pc: a unit that will be controllable by the pc owner. Displayed as blue to the owner and green to others.
#   - enemy: a unit that will be controllable by a gm. Displayed as red.
#   - neutral: a unit that will be controllable by a gm. Displayed as grey.
# Do not edit anything above this line
{
    "name": "",
    "current_health": 0,
    "max_health": 0,
    "controller": "",
    "type": ""
}
                """

                valid_json = False

                while not valid_json:

                    EDITOR = os.environ.get('EDITOR','vim')
                    with tempfile.NamedTemporaryFile(suffix=".json") as tf:
                        tf.write(unit_text.encode("UTF-8"))
                        tf.flush()
                        subprocess.call([EDITOR, tf.name])

                        # do the parsing with `tf` using regular File operations.
                        # for instance:
                        tf.seek(0)
                        unit_text = tf.read().decode("UTF-8")

                        # fix cursor mode
                        curses.curs_set(1)
                        curses.curs_set(0)
                    viewer._draw(force=True) # force redraw after closing vim

                    try:
                        lines = unit_text.splitlines()
                        lines = lines[10:]
                        text = ''.join(lines)
                        unit = json.loads(text)
                        valid_json = True
                    except:
                        pass

                vp = viewer.get_submodule(Viewport)
                c = viewer.get_submodule(Client)

                unit["x"] = vp.cursor_x
                unit["y"] = vp.cursor_y

                c.make_request("/unit/add", payload=unit)

            elif ch == ord("e"):

                vp = viewer.get_submodule(Viewport)

                unit = vp.get_current_unit()

                if unit is not None:

                    unit_text = """
// Name: Name of the unit
// Max Health: the unit's maximum health
// Current Health: the unit's current health, must be less than or equal to max health
// Controller: The owner of the unit. Only the owner and the gm can move the unit.
// Type: The type of the unit, must be one of the following. If not set defaults to neutral.
//   - pc: a unit that will be controllable by the pc owner. Displayed as blue to the owner and green to others.
//   - enemy: a unit that will be controllable by a gm. Displayed as red.
//   - neutral: a unit that will be controllable by a gm. Displayed as grey.
// Do not edit anything above this line"""

                    unit_text = unit_text + "\n" + json.dumps(unit.toDict(edit=True), indent=4, sort_keys=True)

                    valid_json = False

                    while not valid_json:

                        EDITOR = os.environ.get('EDITOR','vim')
                        with tempfile.NamedTemporaryFile(suffix=".json") as tf:
                            tf.write(unit_text.encode("UTF-8"))
                            tf.flush()
                            subprocess.call([EDITOR, tf.name])

                            # do the parsing with `tf` using regular File operations.
                            # for instance:
                            tf.seek(0)
                            unit_text = tf.read().decode("UTF-8")

                            # fix cursor mode
                            curses.curs_set(1)
                            curses.curs_set(0)
                        viewer._draw(force=True) # force redraw after closing vim

                        try:
                            lines = unit_text.splitlines()
                            lines = lines[10:]
                            text = ''.join(lines)
                            unit_updates = json.loads(text)
                            valid_json = True
                        except:
                            pass

                    unit.updateFromDict(unit_updates)

                    c = viewer.get_submodule(Client)

                    c.make_request("/unit/update", payload=unit.toDict())



            elif ch == ord("r"):
                vp = viewer.get_submodule(Viewport)
                c = viewer.get_submodule(Client)

                unit = vp.get_current_unit()


                c.make_request('/unit/rm', payload={
                    "id": unit.id
                })

            elif ch == ord("m"):
                self._mode = CommandMode.unit_move
                self._dirty = True


        elif self._mode is CommandMode.unit_move:
            state = viewer.get_submodule(State)

            if ch == 27 or ch == curses.ascii.ESC: # escape
                self._mode = CommandMode.units
                self._dirty = True

            elif state.get_state("direction_scheme") == "vim":

                vp = viewer.get_submodule(Viewport)
                unit = vp.get_current_unit()

                if ( unit != None and
                        ( unit.controller == state.get_state("username") or
                          state.get_state("role") == "gm" )):
                    if ch == ord("j"):
                        log.error("move unit down")
                        c = viewer.get_submodule(Client)

                        if unit.y+1 <= vp.h:
                            unit.y += 1
                            c.make_request('/unit/update', payload=unit.toDict())
                            vp._dirty = True

                    elif ch == ord("k"):
                        c = viewer.get_submodule(Client)

                        if unit.y-1 >= 1:
                            unit.y -= 1
                            c.make_request('/unit/update', payload=unit.toDict())

                    elif ch == ord("h"):
                        c = viewer.get_submodule(Client)

                        if unit.x-1 >= 1:
                            unit.x -= 1
                            c.make_request('/unit/update', payload=unit.toDict())

                    elif ch == ord("l"):
                        c = viewer.get_submodule(Client)

                        if unit.x+1 <= vp.w:
                            unit.x += 1
                            c.make_request('/unit/update', payload=unit.toDict())
                else:
                    if ch == ord("j"):
                        vp.cursor_up()
                    elif ch == ord("k"):
                        vp.cursor_down()
                    elif ch == ord("h"):
                        vp.cursor_right()
                    elif ch == ord("l"):
                        vp.cursor_left()

            elif state.get_state("direction_scheme") == "wsad":

                vp = viewer.get_submodule(Viewport)
                unit = vp.get_current_unit()

                if ( unit != None and
                        ( unit.controller == state.get_state("username") or
                          state.get_state("role") == "gm" )):
                    if ch == ord("s"):
                        c = viewer.get_submodule(Client)

                        if unit.y+1 <= vp.h:
                            unit.y += 1
                            c.make_request('/unit/update', payload=unit.toDict())
                            vp._dirty = True

                    elif ch == ord("w"):
                        c = viewer.get_submodule(Client)

                        if unit.y-1 >= 1:
                            unit.y -= 1
                            c.make_request('/unit/update', payload=unit.toDict())

                    elif ch == ord("a"):
                        c = viewer.get_submodule(Client)

                        if unit.x-1 >= 1:
                            unit.x -= 1
                            c.make_request('/unit/update', payload=unit.toDict())

                    elif ch == ord("d"):
                        c = viewer.get_submodule(Client)

                        if unit.x+1 <= vp.w:
                            unit.x += 1
                            c.make_request('/unit/update', payload=unit.toDict())
                else:
                    if ch == ord("s"):
                        vp.cursor_up()
                    elif ch == ord("w"):
                        vp.cursor_down()
                    elif ch == ord("a"):
                        vp.cursor_right()
                    elif ch == ord("d"):
                        vp.cursor_left()

        elif self._mode is CommandMode.fow: #gm only
            if ch == 27 or ch == curses.ascii.ESC: # escape
                if self._box:
                    vp = viewer.get_submodule(Viewport)
                    vp.box_xy = None
                    vp._dirty = True

                    self._dirty = True
                    self._box = False
                else:
                    self._mode = CommandMode.default
                    self._dirty = True

            elif ch == ord(" "):
                vp = viewer.get_submodule(Viewport)
                self._box_xy = ( vp.cursor_x, vp.cursor_y )
                vp.box_xy = self._box_xy
                vp._dirty = True
                self._box_referer = self._mode
                self._mode = CommandMode.box_select
                self._dirty = True

            elif ch == ord("a"):
                if self._box:
                    vp = viewer.get_submodule(Viewport)
                    c = viewer.get_submodule(Client)

                    x_min = min(self._box_xy[0], self._box_xy2[0])
                    x_max = max(self._box_xy[0], self._box_xy2[0]) + 1

                    y_min = min(self._box_xy[1], self._box_xy2[1])
                    y_max = max(self._box_xy[1], self._box_xy2[1]) + 1

                    payload = [ {"x": x, "y": y } for x in range(x_min, x_max) for y in range(y_min, y_max) ]
                    c.make_request("/fow/bulk/add", payload={"fow": payload})
                    self._box = False
                    vp.box_xy = None
                    vp._dirty = True

                else:
                    vp = viewer.get_submodule(Viewport)
                    c = viewer.get_submodule(Client)
                    c.make_request("/fow/add", payload={
                        "x": vp.cursor_x,
                        "y": vp.cursor_y
                    })

            elif ch == ord("r"):
                if self._box:
                    vp = viewer.get_submodule(Viewport)
                    c = viewer.get_submodule(Client)

                    x_min = min(self._box_xy[0], self._box_xy2[0])
                    x_max = max(self._box_xy[0], self._box_xy2[0]) + 1

                    y_min = min(self._box_xy[1], self._box_xy2[1])
                    y_max = max(self._box_xy[1], self._box_xy2[1]) + 1

                    payload = [ {"x": x, "y": y } for x in range(x_min, x_max) for y in range(y_min, y_max) ]
                    c.make_request("/fow/bulk/rm", payload={"fow": payload})
                    self._box = False
                    vp.box_xy = None
                    vp._dirty = True

                else:
                    vp = viewer.get_submodule(Viewport)
                    c = viewer.get_submodule(Client)
                    c.make_request("/fow/rm", payload={
                        "x": vp.cursor_x,
                        "y": vp.cursor_y
                    })

            if not self._box:
                if ch == ord("f"):
                    vp = viewer.get_submodule(Viewport)
                    current = state.get_state("fow")
                    if current == "on":
                        state.set_state("fow", "off")
                    else:
                        state.set_state("fow", "on")
                    vp._dirty = True
                    viewer._draw(force=True)


                elif ch == ord("A"):
                    vp = viewer.get_submodule(Viewport)
                    c = viewer.get_submodule(Client)
                    c.make_request("/fow/fill")

                elif ch == ord("R"):
                    vp = viewer.get_submodule(Viewport)
                    c = viewer.get_submodule(Client)
                    c.make_request("/fow/clear")


    def _handle_combo(self, viewer, buff):
            pass

    def _handle_help(self, viewer, buff):
        pass


    def _draw_gm_default_screen(self):
        line = self._draw_title(1, "Commands:")

        line = self._draw_key(line, "b", "Build")
        line = self._draw_key(line, "c", "Chat")
        line = self._draw_key(line, "n", "Narrative")
        line = self._draw_key(line, "f", "Toggle Fog of War for GM")
        line = self._draw_key(line, "F", "Edit Fog of War")
        line = self._draw_key(line, "u", "Units")
        line = self._draw_key(line, "m", "Maps")
        line = self._draw_key(line, "U", "Users")

    def _draw_pc_default_screen(self):
        line = self._draw_title(1, "Commands:")

        line = self._draw_key(line, "c", "Chat")
        line = self._draw_key(line, "u", "Units")

    def _draw_fow_screen(self):
        if self._box:
            line = self._draw_title(1, "Fog of War(Box Mode):")
        else:
            line = self._draw_title(1, "Fog of War:")

        if not self._box:
            line = self._draw_key(line, "f", "Toggle FoW for GM")

        line = self._draw_key(line, "a", "Add FoW")
        line = self._draw_key(line, "r", "Remove FoW")

        if not self._box:
            line = self._draw_key(line, "A", "Fill Map with FoW")
            line = self._draw_key(line, "R", "Clear FoW")
            line = self._draw_key(line+1, "space", "Start Box Mode")

        if self._box:
            line = self._draw_key(line+1, "esc", "Cancel")
        else:
            line = self._draw_key(line+1, "esc", "Back")

    def _draw_units_screen(self, viewer):
        state = viewer.get_submodule(State)
        role = state.get_state("role")
        vp = viewer.get_submodule(Viewport)

        current_unit = vp.get_current_unit()

        if role == "gm":
            line = self._draw_title(1, "Unites:")

            line = self._draw_key(line, "a", "Add Unit")

            if current_unit != None:
                line = self._draw_key(line, "r", "Remove Unit")
                line = self._draw_key(line, "m", "Move Unit")
                line = self._draw_key(line, "e", "Edit Unit")
                line = self._draw_key(line, "+", "Increase Unit Health")
                line = self._draw_key(line, "-", "Decrease Unit Health")

            else:

                line = self._draw_key(line, "m", "Move Unit", colors.get("Dark Grey"))
                line = self._draw_key(line, "e", "Edit Unit", colors.get("Dark Grey"))
                line = self._draw_key(line, "+", "Increase Unit Health", colors.get("Dark Grey"))
                line = self._draw_key(line, "-", "Decrease Unit Health", colors.get("Dark Grey"))

            line = self._draw_key(line+1, "esc", "Back")

        elif role == "pc":
            line = self._draw_title(1, "Unites:")

            if current_unit != None:
                line = self._draw_key(line, "m", "Move Unit")
            else:
                line = self._draw_key(line, "m", "Move Unit", colors.get("Dark Grey"))

            line = self._draw_key(line+1, "esc", "Back")

    def _draw_unit_move_screen(self, viewer):

        state = viewer.get_submodule(State)

        direction_scheme = state.get_state("direction_scheme")

        line = self._draw_title(1, "Move Units:")

        if direction_scheme == "vim":
            line = self._draw_key(line, "j", "Down")
            line = self._draw_key(line, "k", "Up")
            line = self._draw_key(line, "h", "Left")
            line = self._draw_key(line, "l", "Right")

        elif direction_scheme == "wsad":
            line = self._draw_key(line, "s", "Down")
            line = self._draw_key(line, "w", "Up")
            line = self._draw_key(line, "a", "Left")
            line = self._draw_key(line, "d", "Right")

        # esc
        line = self._draw_key(line, "esc", "Back")


    def _draw_build_screen(self):

        if self._box:
            line = self._draw_title(1, "Build (Box Mode):")
        else:
            line = self._draw_title(1, "Build:")

        for binding in sorted(keybindings.build, key=lambda x: x["type"]["name"]):
            line = self._draw_key(line, binding["key"], binding["type"]["name"])

        line = self._draw_key(line+1, "x", "Remove Object")
        line = self._draw_key(line, "space", "Select box corner")

        # esc
        if self._box:
            line = self._draw_key(line+2, "esc", "Cancel Box Mode")
        else:
            line = self._draw_key(line+2, "esc", "Back")


    def _draw_box_select_screen(self):
        line = self._draw_title(1, "Box Select:")

        line = self._draw_key(line, "space", "Select box corner")
        line = self._draw_key(line, "esc", "Cancel")

    def _draw_title(self, line_no, text):
        offset_width = self.w - 4
        n = offset_width
        text = [ text[i:i+n] for i in range(0, len(text), n) ]
        for line in text:
            self._screen.addstr(line_no, 2, line, colors.get("Gold"))
            line_no += 1
        return line_no


    def _draw_key(self, line_no, key, description, attr=None):

        if attr is None:
            self._screen.addstr(line_no, 2, key, colors.get("Gold"))
        else:
            self._screen.addstr(line_no, 2, key, attr)

        key_len = 4 + len(key)
        offset_width = self.w - key_len

        text = ": %s" % description

        n = offset_width
        text = [ text[i:i+n] for i in range(0, len(text), n) ]

        first_line = text.pop(0)
        self._screen.addstr(line_no, 2 + len(key), first_line)
        line_no += 1

        for line in text:
            self._screen.addstr(line_no, 2, line)
            line_no += 1

        return line_no

