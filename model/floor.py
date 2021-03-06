import copy
import tcod
from model.dungeon_tile import DungeonTile
from view.canvas_tile import CanvasTile
from model.components.player_component import PlayerComponent
from model.components.stair_component import StairComponent

class Floor:
    defaul_dungeon_tile = DungeonTile(CanvasTile(tcod.Color(0, 0, 0), tcod.Color(255, 255, 255), ' '), False)

    def __init__(self, width, height, floor):
        self.width = width
        self.height = height
        self.__body = floor
        self.__entities = []

    def get_tile(self, x, y):
        return self.__body[x][y]

    def add_entity(self, new_entity, should_force=False):
        for entity in self.__entities:
            if (new_entity.x == entity.x and new_entity.y == entity.y
                and (self.can_move_into_tile(new_entity.x, new_entity.y) and (not entity.get_component(StairComponent) and not new_entity.get_component(PlayerComponent)))):
                if not should_force:
                    return
                new_entity_position = __find_open_adjacent(new_entity.x, new_entity.y)
                if not new_entity_position:
                    raise(Exception("Cannot add entity " + new_entity.name + " at " + new_entity.x + ", " + new_entity.y + ": obstructed"))
                    return #if there are really no open spaces
                new_entity.x = new_entity_position[0]
                new_entity.y = new_entity_position[1]
        self.__entities.append(new_entity)

    def __find_open_adjacent(start_x, start_y):
        return None
        #TODO!!!!

    def get_entities_in_tile(self, x, y):
        return [entity for entity in self.__entities if entity.x == x and entity.y == y]

    def can_move_into_tile(self, x, y):
        for entity in self.__entities:
            if (self.get_tile(x, y).is_obstacle
                or entity.x == x and entity.y == y and entity.obstructs):
                return False
        return True

    def remove_entity(self, entity):
        self.__entities.remove(entity)

    def get_entity(self, name):
        return next((entity for entity in self.__entities if entity.name == name), None)

    def get_entities(self):
        return self.__entities
