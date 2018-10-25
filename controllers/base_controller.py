from abc import ABC, abstractmethod
from view.panel_canvas import PanelCanvas

class BasePanelController(ABC):

    def __init__(self):
        super().__init__()

    def init_canvas(self, x, y, width, height):
        self.canvas = PanelCanvas(x, y, width, height)

    @abstractmethod
    def handle_key_event(self, key_event):
        pass

    @abstractmethod
    def handle_mouse_event(self, mouse_event):
        pass
