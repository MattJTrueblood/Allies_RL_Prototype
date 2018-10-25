from abc import ABC, abstractmethod

class BasePanelController(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def handle_key_event(self, key_event):
        pass

    @abstractmethod
    def handle_mouse_event(self, mouse_event):
        pass
