from interactive import InteractiveModule, TextDisplayModule
from text_box import TextBox
import random


class Roll(InteractiveModule, TextDisplayModule):

    def __init__(self):
        pass

    def _handle(self, viewer, ch):
        pass

    def _handle_combo(self, viewer, buff):
        buff = buff.split(" ")
        if buff[0] == "roll" or buff[0] == "r" and len(buff) > 1:
            tb = viewer.get_submodule(TextBox)
            text = self.roll(buff[1])
            tb.set_text(text)


    def _handle_help(self, viewer, buff):
        pass

    def _show(self, viewer):
        pass

    def _hide(self, viewer):
        pass

    def roll(self, buf):
         buf = buf.split("d")

         num = int(buf[0])
         die = int(buf[1])

         out = ""
         rolls = []
         cum = 0
         for x in range(num):
             roll = random.randint(1, die)
             rolls.append(roll)
             cum += roll
             out += "Roll %s: %s (Cumulative: %s)\n" % (x+1, roll, cum)
         out += "\n"
         out += "Avg: %s\n" % (cum/num)
         out += "Mode: %s\n" % (max(set(rolls), key=rolls.count))
         out += "Total: %s\n" % cum

         return out
