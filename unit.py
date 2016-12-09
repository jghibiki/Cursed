import curses
import logging

log = logging.getLogger('simple_example')

class Unit:

    def __init__(self, data):
        self.name = data["name"]
        self.y = data["y"]
        self.x = data["x"]
        self.max_health = data["max_health"]
        self.current_health = data["current_health"]
        self.controller = data["controller"]
        self.type = data["type"]
        self.id = data["id"]

    def draw(self, viewer, screen):
        from state import State
        state = viewer.get_submodule(State)
        role = state.get_state("role")
        username = state.get_state("username")

        if self.controller == username and role != "gm":
            screen.addstr(self.y, self.x, "@", curses.color_pair(5))
        elif self.type == "pc":
            screen.addstr(self.y, self.x, "@", curses.color_pair(3))
        elif self.type == "enemy":
            screen.addstr(self.y, self.x, "@", curses.color_pair(2))
        elif self.type == "neutral" or self.type == "":
            screen.addstr(self.y, self.x, "@", curses.color_pair(0))




    def toDict(self):
        return {
            "name": self.name,
            "y": self.y,
            "x": self.x,
            "max_health": self.max_health,
            "current_health": self.current_health,
            "controller": self.controller,
            "type": self.type,
            "id": self.id
        }
