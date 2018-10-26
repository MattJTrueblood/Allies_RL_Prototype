from abc import ABC, abstractmethod

class Interactive(ABC):

    @abstractmethod
    def interact(self, actor):
        pass

class Visible(ABC):

    @abstractmethod
    def get_canvas_tile(self):
        pass
