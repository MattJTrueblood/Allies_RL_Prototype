from abc import ABC, abstractmethod

class Interactive(ABC):
    @abstractmethod
    def interact(self, actor): pass

class UpdateOnTick(ABC):
    @abstractmethod
    def update(self): pass

    @abstractmethod
    def get_priority(self): pass
