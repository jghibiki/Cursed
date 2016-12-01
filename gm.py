from interactive import InteractiveModule, UserModule
from viewer import ViewerConstants
from screen import Screen
from viewport import Viewport
from editor import Editor
from colon_line import ColonLine
from state import State
import logging
import curses

log = logging.getLogger('simple_example')

class GM(InteractiveModule, UserModule):

    def __init__(self):
        super(GM, self).__init__()

    def _handle_combo(self, viewer, buf):
        pass

    def _handle_help(self, viewer, buf):
        pass

    def _handle(self, viewer, ch):

        screen = viewer.get_submodule(Screen)
        viewport = viewer.get_submodule(Viewport)
        state = viewer.get_submodule(State)
        wsad = state.get_state("direction_scheme")
        wsad = True if wsad is not None and wsad is True else False
        if not wsad:
            if ch == ord("j"):
                self.down(viewer)

            elif ch == ord("k"):
                self.up(viewer)

            elif ch == ord("h"):
                self.left(viewer)

            elif ch == ord("l"):
                self.right(viewer)

            elif ch == ord("J"):
                self.vp_down(viewer)

            elif ch == ord("K"):
                self.vp_up(viewer)

            elif ch == ord("H"):
                self.vp_left(viewer)

            elif ch == ord("L"):
                self.vp_right(viewer)
        else:
            if ch == ord("s"):
                self.down(viewer)

            elif ch == ord("w"):
                self.up(viewer)

            elif ch == ord("a"):
                self.left(viewer)

            elif ch == ord("d"):
                self.right(viewer)

            elif ch == ord("S"):
                self.vp_down(viewer)

            elif ch == ord("W"):
                self.vp_up(viewer)

            elif ch == ord("A"):
                self.vp_left(viewer)

            elif ch == ord("D"):
                self.vp_right(viewer)

        if ch == ord("n"):
            self.edit_note(viewer)

        # some simple utilities
        # TODO: Move these utilities to a dev module
        elif ch == ord("p"):
            import curses
            try:
                for i in range(0, curses.COLORS*curses.COLORS):
                    viewer.screen.addstr(str(i), curses.color_pair(i))
            except:
                pass


        elif ch == ord("P"):
            for i in range(0, 1000):
                self.default_screen.addch(i)


    def up(self, viewer):
        vp = viewer.get_submodule(Viewport)
        vp.cursor_up()

    def down(self, viewer):
        vp = viewer.get_submodule(Viewport)
        vp.cursor_down()

    def left(self, viewer):
        vp = viewer.get_submodule(Viewport)
        vp.cursor_left()

    def right(self, viewer):
        vp = viewer.get_submodule(Viewport)
        vp.cursor_right()

    def vp_down(self, viewer):
        vp = viewer.get_submodule(Viewport)
        screen = viewer.get_submodule(Screen)
        editor = viewer.get_submodule(Editor)
        cl = viewer.get_submodule(ColonLine)
        vp.down()
        editor.down()
        cl.mark_dirty()
        screen.fix_cursor()

    def vp_up(self, viewer):
        vp = viewer.get_submodule(Viewport)
        screen = viewer.get_submodule(Screen)
        editor = viewer.get_submodule(Editor)
        cl = viewer.get_submodule(ColonLine)
        vp.up()
        editor.up()
        cl.mark_dirty()
        screen.fix_cursor()

    def vp_right(self, viewer):
        vp = viewer.get_submodule(Viewport)
        screen = viewer.get_submodule(Screen)
        editor = viewer.get_submodule(Editor)
        cl = viewer.get_submodule(ColonLine)
        vp.right()
        editor.right()
        cl.mark_dirty()
        screen.fix_cursor()

    def vp_left(self, viewer):
        vp = viewer.get_submodule(Viewport)
        screen = viewer.get_submodule(Screen)
        editor = viewer.get_submodule(Editor)
        cl = viewer.get_submodule(ColonLine)
        vp.left()
        editor.left()
        cl.mark_dirty()
        screen.fix_cursor()

    def edit_note(self, viewer):
        import sys, tempfile, os
        import subprocess


        log.error("opening notes")
        vp = viewer.get_submodule(Viewport)
        screen = viewer.get_submodule(Screen)

        idx = vp.get_feature_idx(
                vp.cursor_y,
                vp.cursor_x)

        if idx:
            feature = vp.get_feature(idx)
            notes = feature.notes

            EDITOR = os.environ.get('EDITOR','vim')
            with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
                text = notes.encode("UTF-8")
                tf.write(text)
                tf.flush()
                subprocess.call([EDITOR, tf.name])

                # do the parsing with `tf` using regular File operations.
                # for instance:
                tf.seek(0)
                text = tf.read().decode("UTF-8")

                # fix cursor after opening editor
                curses.curs_set(1)
                curses.curs_set(0)

                # TODO: add a way to upload edited note to server
                feature.notes = text
                vp.update_feature(idx, feature)
            viewer._draw(force=True) # force redraw after closing vim



