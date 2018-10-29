from model.dungeon_tile import DungeonTile
from view.canvas_tile import CanvasTile
from model.entity import Entity
from model.mapgen.base_floor_generator import BaseFloorGenerator
from model.components.stair_component import StairComponent
from model.components.visible_component import VisibleComponent
from model.components.health_component import HealthComponent
from model.components.enemy_component import EnemyComponent
from model.floor import Floor
import tcod
import random

class BlankFloorGenerator(BaseFloorGenerator):

    def generate_floor(self, width, height):

        ####make tiles####

        tiles = [[DungeonTile(CanvasTile(tcod.Color(0, 0, 0), tcod.Color(255, 255, 255), '.'), False) for i in range(height)] for j in range(width)]
        for i in range(width):
            for j in range(height):
                if i == 0 or j == 0 or i == width-1 or j == height-1:
                    tiles[i][j].canvas_tile.character = '#'
                    tiles[i][j].is_obstacle = True

        floor = Floor(width, height, tiles)

        ####populate with necessary entities####

        #Stairs
        up_stair_x = random.randint(1, width-2)
        up_stair_y = random.randint(1, height-2)
        while True:
            down_stair_x = random.randint(1, width-2)
            down_stair_y = random.randint(1, height-2)
            if down_stair_x != up_stair_x or down_stair_y != up_stair_y:
                break
        up_stair = Entity("up_stair", up_stair_x, up_stair_y)
        down_stair = Entity("down_stair", down_stair_x, down_stair_y)
        up_stair.add_component(StairComponent(up_stair, True))
        up_stair.add_component(VisibleComponent(up_stair, CanvasTile(None, tcod.Color(255, 0, 0), '<')))
        down_stair.add_component(StairComponent(up_stair, False))
        down_stair.add_component(VisibleComponent(up_stair, CanvasTile(None, tcod.Color(255, 0, 0), '>')))
        floor.add_entity(up_stair)
        floor.add_entity(down_stair)

        #monsters
        for i in range(random.randint(1,20)):
            monster = Entity("monster " + str(i), random.randint(1, width-2), random.randint(1, height-2), True)
            monster.add_component(EnemyComponent(monster))
            monster.add_component(VisibleComponent(monster, CanvasTile(None, tcod.Color(0, 0, 255), '&')))
            monster.add_component(HealthComponent(monster, 1))
            floor.add_entity(monster)

        return floor
