from model.components.interfaces import UpdateOnTick
from model.components.base_component import BaseComponent
import model.dungeon as dungeon
import random

class EnemyComponent(BaseComponent, UpdateOnTick):

    def __init(self, parent_entity):
        super().__init__(parent_entity)

    def update(self):
        self.move(random.randint(-1, 1), random.randint(-1, 1))

    def move(self, dx, dy):
        new_x = self.parent_entity.x + dx
        new_y = self.parent_entity.y + dy
        if dungeon.current_floor.can_move_into_tile(new_x, new_y):
            for entity in dungeon.current_floor.get_entities():
                if entity.x == new_x and entity.y == new_y:
                    break
            self.parent_entity.x = new_x
            self.parent_entity.y = new_y

    def get_priority(self):
        return 1 #Enemies have a low priority, they will always act after allies or neutrals.
