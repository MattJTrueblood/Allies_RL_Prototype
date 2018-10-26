from abc import ABC, abstractmethod

class Interactive(ABC):
    @abstractmethod
    def interact(self, actor): pass

class UpdateOnTick(ABC):
    @abstractmethod
    def update(self): pass
