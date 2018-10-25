from controllers.base_controller import BasePanelController
import tcod
import time
from random import shuffle

class StartMenuController(BasePanelController):

    def __init__(self):
        super().__init__()

    def init_canvas(self, x, y, width, height):
        super().init_canvas(x, y, width, height)

    def handle_key_event(self, key_event):
        pass #TODO

    def handle_mouse_event(self, mouse_event):
        pass #TODO
