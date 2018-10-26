from model.dungeon_tile import DungeonTile
from view.canvas_tile import CanvasTile
from model.entity import Entity
from model.base_floor_generator import BaseFloorGenerator
from model.components.stair_component import StairComponent
import tcod
import random

class BlankFloorGenerator(BaseFloorGenerator):

    def generate_floor(self, width, height):
        floor = [[DungeonTile(CanvasTile(tcod.Color(0, 0, 0), tcod.Color(255, 255, 255), '.'), False) for i in range(height)] for j in range(width)]
        entities = []

        #make walls
        for i in range(width):
            for j in range(height):
                if i == 0 or j == 0 or i == width-1 or j == height-1:
                    floor[i][j].canvas_tile.character = '#'
                    floor[i][j].is_obstacle = True

        #make stairs
        up_stair_x = random.randint(1, width-2)
        up_stair_y = random.randint(1, height-2)
        while True:
            down_stair_x = random.randint(1, width-2)
            down_stair_y = random.randint(1, height-2)
            if down_stair_x != up_stair_x or down_stair_y != up_stair_y:
                break
        up_stair = Entity("up_stair", up_stair_x, up_stair_y)
        down_stair = Entity("down_stair", down_stair_x, down_stair_y)
        up_stair.add_component(StairComponent(True))
        down_stair.add_component(StairComponent(False))

        entities.append(up_stair)
        entities.append(down_stair)

        return (floor, entities)
