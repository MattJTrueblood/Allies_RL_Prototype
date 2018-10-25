import core

class Panel:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.controller = None

    def set_controller(self, controller):
        self.controller = controller
        self.controller.init_canvas(self.x, self.y, self.width, self.height)

    def render(self):
        self.controller.canvas.render()

    def update(self):
        self.controller.update()

    def handle_key_event(self, key_event):
        if self.controller:
            self.controller.handle_key_event(key_event)

    def handle_mouse_event(self, mouse_event):
        if self.controller:
            self.controller.handle_mouse_event(mouse_event)
