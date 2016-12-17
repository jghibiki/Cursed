import curses
import math

class Colors:


    LIGHT_RED = 20
    RED = 21
    DARK_RED = 22

    LIGHT_BLUE = 23
    BLUE = 24
    DARK_BLUE = 25

    LIGHT_GREEN = 26
    GREEN = 27
    DARK_GREEN = 28

    BROWN = 29

    LIGHT_GREY = 30
    LIGHT_GRAY = 30
    GREY = 31
    GRAY = 31
    DARK_GREY = 32
    DARK_GRAY = 32

    GOLD = 33

    WHITE = 34

    BLACK = 35

    WHITE_ON_BLACK = 35

    ORANGE = 36

    BLUE_ON_LIGHT_BLUE = 37

    RED_ON_ORANGE = 38


    def init():
        curses.start_color()

        Colors.register_color(Colors.WHITE, 255, 255, 255)
        Colors.register_color(Colors.BLACK, 0, 0, 0)

        Colors.register_color(Colors.LIGHT_RED, 255, 118, 118)
        Colors.register_color(Colors.RED, 255, 0, 0)
        Colors.register_color(Colors.DARK_RED, 133, 0, 0)

        Colors.register_color(Colors.LIGHT_GREEN, 118, 255, 118)
        Colors.register_color(Colors.GREEN, 0, 255, 0)
        Colors.register_color(Colors.DARK_GREEN, 0, 133, 0)

        Colors.register_color(Colors.LIGHT_BLUE, 0, 170, 255)
        Colors.register_color(Colors.BLUE, 0, 0, 255)
        Colors.register_color(Colors.DARK_BLUE, 0, 0, 133)

        Colors.register_color(Colors.LIGHT_GREY, 200, 200, 200)
        Colors.register_color(Colors.GREY, 138, 138, 138)
        Colors.register_color(Colors.DARK_GREY, 94, 94, 94)

        Colors.register_color(Colors.BROWN, 145, 73, 0)

        Colors.register_color(Colors.GOLD, 255, 200, 0)

        Colors.register_color(Colors.ORANGE, 255, 150, 0)


        # register white on black
        curses.init_pair(Colors.WHITE_ON_BLACK, Colors.WHITE, Colors.BLACK)

        # complex color combos
        curses.init_pair(Colors.BLUE_ON_LIGHT_BLUE, Colors.BLUE, Colors.LIGHT_BLUE)
        curses.init_pair(Colors.RED_ON_ORANGE, Colors.RED, Colors.ORANGE)

        # set background to black
        curses.init_color(0,
                Colors.scale_color(0),
                Colors.scale_color(0),
                Colors.scale_color(0))

    def scale_color(color):
        return math.ceil((color/255)*1000)

    def register_color(color, r, g, b, bg=None):
        curses.init_color(color,
                Colors.scale_color(r),
                Colors.scale_color(g),
                Colors.scale_color(b))
        if bg is not None:
            curses.init_pair(color, color, bg)
        else:
            curses.init_pair(color, color, Colors.BLACK)



    def get(color):
        return curses.color_pair(color)
