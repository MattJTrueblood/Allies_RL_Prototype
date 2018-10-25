import tcod
import core

class Panel:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def set_bg_color(self, color):
        self.bg_color = color

    def render(self):
        #Default behavior is to fill with background color.
        core.root_console.default_bg = self.bg_color
        tcod.console_rect(core.root_console, self.x, self.y, self.width, self.height, True, True)
