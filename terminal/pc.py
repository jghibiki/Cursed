from interactive import InteractiveModule, UserModule
from viewer import ViewerConstants
from screen import Screen
from viewport import Viewport
from state import State
from colon_line import ColonLine
from text_box import TextBox
import log

log = log.logger

class PC(InteractiveModule, UserModule):
    def __init__(self):
        super(PC, self).__init__()

    def _handle_combo(self, viewer, buf):
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
        cl = viewer.get_submodule(ColonLine)
        vp.down()
        cl.mark_dirty()
        screen.fix_cursor()

    def vp_up(self, viewer):
        vp = viewer.get_submodule(Viewport)
        screen = viewer.get_submodule(Screen)
        cl = viewer.get_submodule(ColonLine)
        vp.up()
        cl.mark_dirty()
        screen.fix_cursor()

    def vp_right(self, viewer):
        vp = viewer.get_submodule(Viewport)
        screen = viewer.get_submodule(Screen)
        cl = viewer.get_submodule(ColonLine)
        vp.right()
        cl.mark_dirty()
        screen.fix_cursor()

    def vp_left(self, viewer):
        vp = viewer.get_submodule(Viewport)
        screen = viewer.get_submodule(Screen)
        cl = viewer.get_submodule(ColonLine)
        vp.left()
        cl.mark_dirty()
        screen.fix_cursor()

