from interactive import VisibleModule, InteractiveModule
from features import FeatureType, Feature, FeatureSerializer
from viewer import ViewerConstants
from viewport import Viewport
from client import Client
from state import State
import logging
import curses
import math

log = logging.getLogger('simple_example')

class CommandMode:
    default = 0
    build = 1


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

        self._count = ""

        self._dirty = True

    def draw(self, viewer, force=False):
        if self._dirty or force:
            if force: log.debug("command_window.draw forced")

            self._screen.clear()

            state = viewer.get_submodule(State)
            self._screen.attrset(curses.color_pair(179))
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
            self._screen.attroff(curses.color_pair(179))

            if self._mode is CommandMode.default: self._draw_default_screen()
            if self._mode is CommandMode.build: self._draw_build_screen()

            self._screen.noutrefresh()
            self._dirty = False
            return True
        return False

    def _handle(self, viewer, ch):

        if self._mode is CommandMode.default:
            if ch == ord("b"):
                self._mode = CommandMode.build
                self._dirty = True

            if ch == ord("c"):
                from chat import Chat
                chat = viewer.get_submodule(Chat)
                chat.show(viewer)

        elif self._mode is CommandMode.build:
            if ch == 27 or ch == curses.ascii.ESC: # escape
                self._mode = CommandMode.default
                self._dirty = True


            elif ch == ord("w"):
                vp = viewer.get_submodule(Viewport)
                c = viewer.get_submodule(Client)
                feature = Feature(vp.cursor_y,
                                  vp.cursor_x,
                                  FeatureType.wall)
                raw_feature = FeatureSerializer.toDict(feature)
                c.make_request("/map/add", payload=raw_feature)

            elif ch == ord("c"):
                vp = viewer.get_submodule(Viewport)
                c = viewer.get_submodule(Client)
                feature = Feature(vp.cursor_y,
                                  vp.cursor_x,
                                  FeatureType.chair)
                raw_feature = FeatureSerializer.toDict(feature)
                c.make_request("/map/add", payload=raw_feature)

            elif ch == ord("d"):
                vp = viewer.get_submodule(Viewport)
                c = viewer.get_submodule(Client)
                feature = Feature(vp.cursor_y,
                                  vp.cursor_x,
                                  FeatureType.door)
                raw_feature = FeatureSerializer.toDict(feature)
                c.make_request("/map/add", payload=raw_feature)

            elif ch == ord("t"):
                vp = viewer.get_submodule(Viewport)
                c = viewer.get_submodule(Client)
                feature = Feature(vp.cursor_y,
                                  vp.cursor_x,
                                  FeatureType.table)
                raw_feature = FeatureSerializer.toDict(feature)
                c.make_request("/map/add", payload=raw_feature)

            elif ch == ord(">"):
                vp = viewer.get_submodule(Viewport)
                c = viewer.get_submodule(Client)
                feature = Feature(vp.cursor_y,
                                  vp.cursor_x,
                                  FeatureType.up_stair)
                raw_feature = FeatureSerializer.toDict(feature)
                c.make_request("/map/add", payload=raw_feature)

            elif ch == ord("<"):
                vp = viewer.get_submodule(Viewport)
                c = viewer.get_submodule(Client)
                feature = Feature(vp.cursor_y,
                                  vp.cursor_x,
                                  FeatureType.down_stair)
                raw_feature = FeatureSerializer.toDict(feature)
                c.make_request("/map/add", payload=raw_feature)

            elif ch == ord("%"):
                vp = viewer.get_submodule(Viewport)
                c = viewer.get_submodule(Client)
                feature = Feature(vp.cursor_y,
                                  vp.cursor_x,
                                  FeatureType.lantern)
                raw_feature = FeatureSerializer.toDict(feature)
                c.make_request("/map/add", payload=raw_feature)

            elif ch == ord("#"):
                vp = viewer.get_submodule(Viewport)
                c = viewer.get_submodule(Client)
                feature = Feature(vp.cursor_y,
                                  vp.cursor_x,
                                  FeatureType.chest)
                raw_feature = FeatureSerializer.toDict(feature)
                c.make_request("/map/add", payload=raw_feature)

            elif ch == ord("*"):
                vp = viewer.get_submodule(Viewport)
                c = viewer.get_submodule(Client)
                feature = Feature(vp.cursor_y,
                                  vp.cursor_x,
                                  FeatureType.point_of_interest)
                raw_feature = FeatureSerializer.toDict(feature)
                c.make_request("/map/add", payload=raw_feature)

            elif ch == ord("r"):
                vp = viewer.get_submodule(Viewport)
                c = viewer.get_submodule(Client)
                feature = Feature(vp.cursor_y,
                                  vp.cursor_x,
                                  FeatureType.road)
                raw_feature = FeatureSerializer.toDict(feature)
                c.make_request("/map/add", payload=raw_feature)

            elif ch == ord("G"):
                vp = viewer.get_submodule(Viewport)
                c = viewer.get_submodule(Client)
                feature = Feature(vp.cursor_y,
                                  vp.cursor_x,
                                  FeatureType.gate)
                raw_feature = FeatureSerializer.toDict(feature)
                c.make_request("/map/add", payload=raw_feature)

            elif ch == ord("W"):
                vp = viewer.get_submodule(Viewport)
                c = viewer.get_submodule(Client)
                feature = Feature(vp.cursor_y,
                                  vp.cursor_x,
                                  FeatureType.water)
                raw_feature = FeatureSerializer.toDict(feature)
                c.make_request("/map/add", payload=raw_feature)

            elif ch == ord("T"):
                vp = viewer.get_submodule(Viewport)
                c = viewer.get_submodule(Client)
                feature = Feature(vp.cursor_y,
                                  vp.cursor_x,
                                  FeatureType.tree)
                raw_feature = FeatureSerializer.toDict(feature)
                c.make_request("/map/add", payload=raw_feature)

            elif ch == ord("o"):
                vp = viewer.get_submodule(Viewport)
                c = viewer.get_submodule(Client)
                feature = Feature(vp.cursor_y,
                                  vp.cursor_x,
                                  FeatureType.bush)
                raw_feature = FeatureSerializer.toDict(feature)
                c.make_request("/map/add", payload=raw_feature)

            elif ch == ord("."):
                vp = viewer.get_submodule(Viewport)
                c = viewer.get_submodule(Client)
                feature = Feature(vp.cursor_y,
                                  vp.cursor_x,
                                  FeatureType.grass)
                raw_feature = FeatureSerializer.toDict(feature)
                c.make_request("/map/add", payload=raw_feature)

            elif ch == ord(","):
                vp = viewer.get_submodule(Viewport)
                c = viewer.get_submodule(Client)
                feature = Feature(vp.cursor_y,
                                  vp.cursor_x,
                                  FeatureType.friendly_unit)
                raw_feature = FeatureSerializer.toDict(feature)
                c.make_request("/map/add", payload=raw_feature)

            elif ch == ord("@"):
                vp = viewer.get_submodule(Viewport)
                c = viewer.get_submodule(Client)
                feature = Feature(vp.cursor_y,
                                  vp.cursor_x,
                                  FeatureType.enemy_unit)
                raw_feature = FeatureSerializer.toDict(feature)
                c.make_request("/map/add", payload=raw_feature)

            elif ch == ord("$"):
                vp = viewer.get_submodule(Viewport)
                c = viewer.get_submodule(Client)
                feature = Feature(vp.cursor_y,
                                  vp.cursor_x,
                                  FeatureType.dead_unit)
                raw_feature = FeatureSerializer.toDict(feature)
                c.make_request("/map/add", payload=raw_feature)

            elif ch == ord("^"):
                vp = viewer.get_submodule(Viewport)
                c = viewer.get_submodule(Client)
                feature = Feature(vp.cursor_y,
                                  vp.cursor_x,
                                  FeatureType.hill)
                raw_feature = FeatureSerializer.toDict(feature)
                c.make_request("/map/add", payload=raw_feature)


    def _handle_combo(self, viewer, buff):
            pass

    def _handle_help(self, viewer, buff):
        pass


    def _draw_default_screen(self):
        self._screen.addstr(1, 2, "Commands:", curses.color_pair(179))

        # build menu
        self._screen.addstr(2, 2, "b", curses.color_pair(179))
        self._screen.addstr(2, 3, ": Build", )

        # show chat
        self._screen.addstr(3, 2, "c", curses.color_pair(179))
        self._screen.addstr(3, 3, ": Chat", )

    def _draw_build_screen(self):
        self._screen.addstr(1, 2, "Build:", curses.color_pair(179))


        # wall
        self._screen.addstr(2, 2, "w", curses.color_pair(179))
        self._screen.addstr(2, 3, ": Wall(")
        self._screen.addstr(2, 10,
                FeatureType.toSymbol(
                    FeatureType.wall),
                FeatureType.modFromName(
                    FeatureType.toName(
                        FeatureType.wall)))
        self._screen.addstr(2, 11, ")")

        # water
        self._screen.addstr(3, 2, "W", curses.color_pair(179))
        self._screen.addstr(3, 3, ": Water(")
        self._screen.addstr(3, 11,
                FeatureType.toSymbol( FeatureType.water ),
                FeatureType.modFromName(
                    FeatureType.toName(
                        FeatureType.water)))
        self._screen.addstr(3, 12, ")")

        # door
        self._screen.addstr(4, 2, "d", curses.color_pair(179))
        self._screen.addstr(4, 3, ": Door(")
        self._screen.addstr(4, 10,
                FeatureType.toSymbol( FeatureType.door ),
                FeatureType.modFromName(
                    FeatureType.toName(
                        FeatureType.door)))
        self._screen.addstr(4, 11, ")")

        # gate
        self._screen.addstr(5, 2, "G", curses.color_pair(179))
        self._screen.addstr(5, 3, ": Gate(")
        self._screen.addstr(5, 10,
                FeatureType.toSymbol( FeatureType.gate ),
                FeatureType.modFromName(
                    FeatureType.toName(
                        FeatureType.gate)))
        self._screen.addstr(5, 11, ")")

        # Road
        self._screen.addstr(6, 2, "r", curses.color_pair(179))
        self._screen.addstr(6, 3, ": Road(")
        self._screen.addstr(6, 10,
                FeatureType.toSymbol( FeatureType.road ),
                FeatureType.modFromName(
                    FeatureType.toName(
                        FeatureType.road)))
        self._screen.addstr(6, 11, ")")

        # bush
        self._screen.addstr(7, 2, "o", curses.color_pair(179))
        self._screen.addstr(7, 3, ": Bush(")
        self._screen.addstr(7, 10,
                FeatureType.toSymbol( FeatureType.bush ),
                FeatureType.modFromName(
                    FeatureType.toName(
                        FeatureType.bush)))
        self._screen.addstr(7, 11, ")")

        # grass
        self._screen.addstr(8, 2, ".", curses.color_pair(179))
        self._screen.addstr(8, 3, ": Grass(")
        self._screen.addstr(8, 11,
                FeatureType.toSymbol( FeatureType.grass ),
                FeatureType.modFromName(
                    FeatureType.toName(
                        FeatureType.grass)))
        self._screen.addstr(8, 12, ")")

        # table
        self._screen.addstr(9, 2, "t", curses.color_pair(179))
        self._screen.addstr(9, 3, ": Table(")
        self._screen.addstr(9, 11,
                FeatureType.toSymbol( FeatureType.table ),
                FeatureType.modFromName(
                    FeatureType.toName(
                        FeatureType.table)))
        self._screen.addstr(9, 12, ")")

        # chair
        self._screen.addstr(10, 2, "t", curses.color_pair(179))
        self._screen.addstr(10, 3, ": Chair(")
        self._screen.addstr(10, 11,
                FeatureType.toSymbol( FeatureType.chair),
                FeatureType.modFromName(
                    FeatureType.toName(
                        FeatureType.chair)))
        self._screen.addstr(10, 12, ")")

        # tree
        self._screen.addstr(11, 2, "T", curses.color_pair(179))
        self._screen.addstr(11, 3, ": Tree(")
        self._screen.addstr(11, 10,
                FeatureType.toSymbol( FeatureType.tree ),
                FeatureType.modFromName(
                    FeatureType.toName(
                        FeatureType.tree)))
        self._screen.addstr(11, 11, ")")

        # hill
        self._screen.addstr(12, 2, "^", curses.color_pair(179))
        self._screen.addstr(12, 3, ": Hill(")
        self._screen.addstr(12, 10,
                FeatureType.toSymbol( FeatureType.hill ),
                FeatureType.modFromName(
                    FeatureType.toName(
                        FeatureType.hill)))
        self._screen.addstr(12, 11, ")")

        # Up stair/Ladder
        self._screen.addstr(13, 2, ">", curses.color_pair(179))
        self._screen.addstr(13, 3, ": Up Stair/Ladder(")
        self._screen.addstr(13, 21,
                FeatureType.toSymbol( FeatureType.up_stair ),
                FeatureType.modFromName(
                    FeatureType.toName(
                        FeatureType.up_stair)))
        self._screen.addstr(13, 22, ")")

        # Down stair/ladder
        self._screen.addstr(14, 2, "<", curses.color_pair(179))
        self._screen.addstr(14, 3, ": Down Stair/Ladder(")
        self._screen.addstr(14, 23,
                FeatureType.toSymbol( FeatureType.down_stair ),
                FeatureType.modFromName(
                    FeatureType.toName(
                        FeatureType.down_stair)))
        self._screen.addstr(14, 24, ")")

        # lantern
        self._screen.addstr(15, 2, "%", curses.color_pair(179))
        self._screen.addstr(15, 3, ": Lantern(")
        self._screen.addstr(15, 13,
                FeatureType.toSymbol( FeatureType.lantern ),
                FeatureType.modFromName(
                    FeatureType.toName(
                        FeatureType.lantern)))
        self._screen.addstr(15, 14, ")")

        # chest
        self._screen.addstr(16, 2, "#", curses.color_pair(179))
        self._screen.addstr(16, 3, ": Chest(")
        self._screen.addstr(16, 11,
                FeatureType.toSymbol( FeatureType.lantern ),
                FeatureType.modFromName(
                    FeatureType.toName(
                        FeatureType.lantern)))
        self._screen.addstr(16, 12, ")")

        # point of interest *
        self._screen.addstr(17, 2, "*", curses.color_pair(179))
        self._screen.addstr(17, 3, ": Point Of Interest(")
        self._screen.addstr(17, 23,
                FeatureType.toSymbol( FeatureType.point_of_interest),
                FeatureType.modFromName(
                    FeatureType.toName(
                        FeatureType.point_of_interest)))
        self._screen.addstr(17, 24, ")")

        # friendly unit ,
        self._screen.addstr(18, 2, ",", curses.color_pair(179))
        self._screen.addstr(18, 3, ": Friendly Unit(")
        self._screen.addstr(18, 19,
                FeatureType.toSymbol( FeatureType.friendly_unit),
                FeatureType.modFromName(
                    FeatureType.toName(
                        FeatureType.friendly_unit)))
        self._screen.addstr(18, 20, ")")

        # enemy unit @
        self._screen.addstr(19, 2, ",", curses.color_pair(179))
        self._screen.addstr(19, 3, ": Enemy Unit(")
        self._screen.addstr(19, 16,
                FeatureType.toSymbol( FeatureType.enemy_unit),
                FeatureType.modFromName(
                    FeatureType.toName(
                        FeatureType.enemy_unit)))
        self._screen.addstr(19, 17, ")")

        # dead unit $
        self._screen.addstr(20, 2, ",", curses.color_pair(179))
        self._screen.addstr(20, 3, ": Dead Unit(")
        self._screen.addstr(20, 15,
                FeatureType.toSymbol( FeatureType.dead_unit),
                FeatureType.modFromName(
                    FeatureType.toName(
                        FeatureType.dead_unit)))
        self._screen.addstr(20, 16, ")")

        # esc
        self._screen.addstr(23, 2, "esc", curses.color_pair(179))
        self._screen.addstr(23, 6, ": Back", )

