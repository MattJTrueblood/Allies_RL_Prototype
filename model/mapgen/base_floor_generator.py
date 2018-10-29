from abc import ABC, abstractmethod

class BaseFloorGenerator(ABC):

    @abstractmethod
    def generate_floor(self, width, height):
        pass
