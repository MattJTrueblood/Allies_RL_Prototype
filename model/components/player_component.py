import model.dungeon as dungeon
from view.canvas_tile import CanvasTile
from model.components.interfaces import Visible
import tcod

class PlayerComponent(Visible):
    def __init__(self, parent_entity):
        self.entity = parent_entity
        self.canvas_tile = CanvasTile(None, tcod.Color(0,255,0), '@')

    def move(self, dir):
        #convert direction (numpad keys for now) into (x, y)
        if not dungeon.current_floor.get_tile(self.entity.x+dir[0], self.entity.y + dir[1]).is_obstacle:
            self.entity.x += dir[0]
            self.entity.y += dir[1]

    def interact(self):
        dungeon.current_floor.interact(self.entity.x, self.entity.y)

    def set_position(self, x, y):
        self.entity.x = x
        self.entity.y = y

    def get_canvas_tile(self):
        return self.canvas_tile
