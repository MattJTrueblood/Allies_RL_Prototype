from model.components.base_component import BaseComponent
import model.dungeon as dungeon
from view.canvas_tile import CanvasTile
import tcod

class PlayerComponent(BaseComponent):

    def move(self, dx, dy):
        if not dungeon.current_floor.get_tile(self.parent_entity.x + dx, self.parent_entity.y + dy).is_obstacle:
            self.parent_entity.x += dx
            self.parent_entity.y += dy

    def interact(self):
        dungeon.current_floor.interact(self.entity.x, self.entity.y)

    def set_position(self, x, y):
        self.parent_entity.x = x
        self.parent_entity.y = y
