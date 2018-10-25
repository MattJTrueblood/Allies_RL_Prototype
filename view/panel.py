import tcod
import core

class Panel:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.controller = None
        self.bg_color = None

    def set_controller(self, controller):
        self.controller = controller

    def set_bg_color(self, color):
        self.bg_color = color

    def render(self):
        #Default behavior is to fill with background color.
        core.root_console.default_bg = self.bg_color
        tcod.console_rect(core.root_console, self.x, self.y, self.width, self.height, True, True)

    def handle_key_event(self, key_event):
        if self.controller:
            self.controller.handle_key_event(key_event)

    def handle_mouse_event(self, mouse_event):
        if self.controller:
            self.controller.handle_mouse_event(mouse_event)
