from model.components.interfaces import UpdateOnTick
from model.components.base_component import BaseComponent

class AI(BaseComponent, UpdateOnTick):

    def __init(self, parent_entity):
        super().__init__(parent_entity)

    def update(self):
        print("updating!")
