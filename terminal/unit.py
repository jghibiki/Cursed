import log
import colors

log = log.logger

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
            screen.addstr(self.y, self.x, "@", colors.get("Light Blue"))
        elif self.type == "pc":
            screen.addstr(self.y, self.x, "@", colors.get("Light Green"))
        elif self.type == "enemy":
            screen.addstr(self.y, self.x, "@", colors.get("Light Red"))
        elif self.type == "neutral" or self.type == "":
            screen.addstr(self.y, self.x, "@", colors.get("Light Grey"))




    def toDict(self, edit=False):
        if not edit:
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
        else:
            return {
                "name": self.name,
                "max_health": self.max_health,
                "current_health": self.current_health,
                "controller": self.controller,
                "type": self.type,
            }

    def updateFromDict(self, data):
        self.name = data["name"]
        self.max_health = data["max_health"]
        self.current_health = data["current_health"]
        self.controller = data["controller"]
        self.type = data["type"]
