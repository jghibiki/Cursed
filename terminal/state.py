from interactive import InteractiveModule

class State(InteractiveModule):

    def __init__(self):
        self._state={
                "fow": "on",
                "ignore_direction_keys": "off"
        }

    def _handle(self, viewer, ch):
        pass

    def _handle_combo(self, viewer, buff):

        buff = buff.split(" ")
        if ( len(buff) == 3 and
             buff[0] == "set" ):

            self.set_state(buff[1], buff[2])

    def _handle_help(self, viewer, buf):
        pass

    def get_state(self, key):
        if key in self._state:
            return self._state[key]
        return None

    def set_state(self, key, value):
        self._state[key] = value
