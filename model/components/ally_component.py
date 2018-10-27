from model.components.base_component import BaseComponent
from model.components.interfaces import UpdateOnTick

class AllyComponent(BaseComponent, UpdateOnTick):

    def __init__(self, parent_entity):
        super().__init__(parent_entity)

    def update(self):
        pass

    def get_priority(self):
        pass
