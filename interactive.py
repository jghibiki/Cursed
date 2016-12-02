

class InteractiveModule:
    def _handle(self, viewer, ch):
        raise Exception("_handle has not been implemented.")

    def _handle_help(self, viewer, buf):
        raise Exception("_handle_help has not been implemented.")

    def _handle_combo(self, viewer, buf):
        raise Exception("_handle_como has not been implemented.")

class LiveModule:
    def _each(self, viewer):
        raise Exception("_each has not been implemented.")

class TextDisplayModule:
    def _show(self, viewer):
        raise Exception("_show has not been implemented.")

    def _hide(self, viewer):
        raise Exception("_hide has not been implemented.")


class VisibleModule:
    def draw(self):
        raise Exception("draw has not been implemented.")

    def up(self):
        raise Exception("up not been implemented.")

    def down(self):
        raise Exception("down not been implemented.")

    def left(self):
        raise Exception("left not been implemented.")

    def right(self):
        raise Exception("right not been implemented.")


class FeatureModule:
    def add_feature(self):
        raise Exception("add_feature has not been implemented.")

    def rm_feature(self):
        raise Exception("rm_feature has not been implemented.")

    def get_feature_idx(self):
        raise Exception("get_feature_idx has not been implemented.")

    def serialize_features(self):
        raise Exception("serialize_feautes has not been implemented.")


class SavableModule:
    def save(self):
        raise Exception("save has not been implemented.")


class UserModule:

    def up(self):
        raise Exception("up has not been implemented.")

    def down(self):
        raise Exception("down has not been implemented.")

    def left(self):
        raise Exception("left has not been implemented.")

    def right(self):
        raise Exception("right has not been implemented.")


    def vp_up(self):
        raise Exception("vp_up has not been implemented.")

    def vp_down(self):
        raise Exception("vp_down has not been implemented.")

    def vp_left(self):
        raise Exception("vp_left has not been implemented.")

    def vp_right(self):
        raise Exception("vp_right has not been implemented.")


class NetworkModule:
    pass

class ServerModule(NetworkModule):
    def update(self):
        raise Exception("update has not been implemented.")


class ClientModule(NetworkModule):
    def connect(self):
        raise Exception("update has not been implemented.")

    def disconnect(self):
        raise Exception("update has not been implemented.")

    def update(self):
        raise Exception("update has not been implemented.")


