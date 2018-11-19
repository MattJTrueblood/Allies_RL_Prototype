from abc import ABC, abstractmethod

class GroundInteractive(ABC):
    @abstractmethod
    def interact_ground(self, actor): pass

class AdjacentInteractive(ABC):
    @abstractmethod
    def interact_adjacent(self, actor): pass

class MoveInteractive(ABC):
    @abstractmethod
    def interact_move(self, actor): pass

class UpdateOnTick(ABC):
    @abstractmethod
    def update(self): pass

    @abstractmethod
    def get_priority(self): pass
