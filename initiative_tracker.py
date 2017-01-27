from interactive import  InteractiveModule, TextDisplayModule
from viewport import Viewport
from text_box import TextBox
import random
import json
import curses
import logging

log = logging.getLogger('simple_example')

class InitiativeTracker(InteractiveModule, TextDisplayModule):

    def __init__(self):
        self._showing = False

        self.init_units = []


    def _handle(self, viewer, ch):
        if ch == ord("I"):
            vp = viewer.get_submodule(Viewport)


            self.init_units = []
            for unit in vp._units:
                self.init_units.append({
                    "include": False,
                    "name": unit.name,
                    "id": unit.id,
                    "modifier": 0
                })

            text = json.dumps(self.init_units, indent=4)

            import sys, tempfile, os
            import subprocess

            EDITOR = os.environ.get('EDITOR','vim')
            with tempfile.NamedTemporaryFile(suffix=".md") as tf:
                text = text.encode("UTF-8")
                tf.write(text)
                tf.flush()
                subprocess.call([EDITOR, tf.name])

                # do the parsing with `tf` using regular File operations.
                # for instance:
                tf.seek(0)
                out_text = tf.read().decode("UTF-8")

                # fix cursor after opening editor
                curses.curs_set(1)
                curses.curs_set(0)

                self.init_units = json.loads(out_text)

            viewer._draw(force=True) # force redraw after closing vim


            included = []
            for unit in self.init_units:
                log.error(unit)
                if unit["include"]:
                    included.append(unit)

            log.error(included)
            self.init_units = included

            for unit in self.init_units:
                unit["roll"] = unit["modifier"] + random.randint(0, 20)

            self.init_units = sorted(self.init_units, key=lambda x: x["roll"], reverse=True)

            viewer.apply_to_submodules(TextDisplayModule, lambda x: x._hide(viewer))
            self._show(viewer)

        elif ch == ord("i"):
            viewer.apply_to_submodules(TextDisplayModule, lambda x: x._hide(viewer))
            self._show(viewer)



    def _handle_help(self, viewer, buf):
        pass

    def _handle_combo(self, viewer, buf):
        split = buf.split(" ")

        if split[0] == "init" and ( split[1] == "roll" or split[1] == "r" ):
            for unit in self.init_units:
                unit["roll"] = unit["modifier"] + random.randint(0, 20)

            self.init_units = sorted(self.init_units, key=lambda x: x["roll"], reverse=True)
            self._show(viewer)



    def _show(self, viewer):
        self._showing = True

        tb = viewer.get_submodule(TextBox)

        lines = [ [{
            "text": "Initiative:",
            "color": "Gold"
        }] ]

        for unit in self.init_units:
            lines.append([ {
                "text": "{0} - {1}".format(unit["roll"], unit["name"]),
                "color": None
            } ])

        log.error(lines)
        tb.set(lines)

    def _hide(self, viewer):
        self._showing = False




