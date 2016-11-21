from interactive import InteractiveModule, UserModule
from viewer import ViewerConstants
from screen import Screen
from viewport import Viewport

class GM(InteractiveModule, UserModule):

    def __init__(self):
        super(GM, self).__init__()

    def _handle_combo(self, viewer, buf):
        if "w" in buf:
            json_map = self.map.serialize()
            self.save_handler(json_map)

    def _handle(self, viewer, ch):

        screen = viewer.get_submodule(Screen)
        viewport = viewer.get_submodule(Viewport)

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

        elif ch == ord("n"):
            self.edit_note(viewer)

        # some simple utilities
        elif ch == ord("p"):
            for i in range(0, 255):
                self.default_screen.addstr(str(i), curses.color_pair(i))

        elif ch == ord("P"):
            for i in range(0, 1000):
                self.default_screen.addch(i)


    def up(self, viewer):
        screen = viewer.get_submodule(Screen)
        if screen.y - 1 >= ViewerConstants.min_y+2:
            screen.up()

    def down(self, viewer):
        screen = viewer.get_submodule(Screen)
        if screen.y + 1 <= ViewerConstants.max_y-1:
            screen.down()

    def left(self, viewer):
        screen = viewer.get_submodule(Screen)
        if screen.x - 1 >= ViewerConstants.min_x+1:
            screen.left()

    def right(self, viewer):
        screen = viewer.get_submodule(Screen)
        if screen.x + 1 <= ViewerConstants.max_x-1:
            screen.right()

    def vp_down(self, viewer):
        vp = viewer.get_submodule(Viewport)
        screen = viewer.get_submodule(Screen)
        vp.move_vp_down()
        screen.fix_cursor()

    def vp_up(self, viewer):
        vp = viewer.get_submodule(Viewport)
        screen = viewer.get_submodule(Screen)
        vp.move_vp_up()
        screen.fix_cursor()

    def vp_right(self, viewer):
        vp = viewer.get_submodule(Viewport)
        screen = viewer.get_submodule(Screen)
        vp.move_vp_right()
        screen.fix_cursor()

    def vp_left(self, viewer):
        vp = viewer.get_submodule(Viewport)
        screen = viewer.get_submodule(Screen)
        vp.move_vp_left()
        screen.fix_cursor()

    def edit_note(self, viewer):
        vp = viewer.get_submodule(Viewport)
        screen = viewer.get_submodule(Screen)

        idx = vp.get_feature_idx(
                screen.y + vp.y - 1,
                screen.x + vp.x)

        if idx:
            feature = vp.get_feature(idx)
            notes = feature.notes

            textbox = screen.make_textbox(
                    5, 5,
                    ViewerConstants.max_y-10,
                    ViewerConstants.max_x-10,
                    deco="frame", value=notes)
            text = textbox.edit()
            feature.notes = text
            vp.update_feature(idx, feature)



