import logging
from colors import Colors

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
            screen.addstr(self.y, self.x, "@", Colors.get(Colors.LIGHT_BLUE))
        elif self.type == "pc":
            screen.addstr(self.y, self.x, "@", Colors.get(Colors.LIGHT_GREEN))
        elif self.type == "enemy":
            screen.addstr(self.y, self.x, "@", Colors.get(Colors.LIGHT_RED))
        elif self.type == "neutral" or self.type == "":
            screen.addstr(self.y, self.x, "@", Colors.get(Colors.LIGHT_GREY))




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
