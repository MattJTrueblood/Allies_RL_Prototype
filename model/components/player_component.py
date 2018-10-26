from model.components.base_component import BaseComponent
import model.dungeon as dungeon
from view.canvas_tile import CanvasTile
import tcod
import core

class PlayerComponent(BaseComponent):

    def move(self, dx, dy):
        if (not dungeon.current_floor.get_tile(self.parent_entity.x + dx, self.parent_entity.y + dy).is_obstacle
            and not next((entity for entity in dungeon.current_floor.get_entities()
            if entity.obstructs and entity.x == self.parent_entity.x + dx and entity.y == self.parent_entity.y + dy), False)):
            self.set_position(self.parent_entity.x + dx, self.parent_entity.y + dy)
            core.master_tick += 1

    def interact(self):
        dungeon.current_floor.interact(self.entity.x, self.entity.y)
        core.master_tick += 1

    def set_position(self, x, y):
        self.parent_entity.x = x
        self.parent_entity.y = y
