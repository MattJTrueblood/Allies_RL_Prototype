import copy
import tcod
from model.dungeon_tile import DungeonTile
from view.canvas_tile import CanvasTile

class Floor:
    defaul_dungeon_tile = DungeonTile(CanvasTile(tcod.Color(0, 0, 0), tcod.Color(255, 255, 255), ' '), False)

    def __init__(self, width, height, floor_generator):
        self.width = width
        self.height = height
        generated_floor = floor_generator.generate_floor(width, height)
        self.__body = generated_floor[0]
        self.entities = generated_floor[1]

    def get_tile(self, x, y):
        return self.__body[x][y]

    def get_entity(self, name):
        return next((entity for entity in self.entities if entity.name == name), None)
