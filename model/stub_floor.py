from view.canvas_tile import CanvasTile
from model.dungeon_tile import DungeonTile
import tcod

class StubFloor:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__body = [[DungeonTile(CanvasTile(tcod.Color(0, 0, 0), tcod.Color(255, 255, 255), '.'), False) for i in range(height)] for j in range(width)]
        #draw border
        for i in range(width):
            for j in range(height):
                if i == 0 or j == 0 or i == width-1 or j == height-1:
                    self.__body[i][j].canvas_tile.character = '#'
                    self.__body[i][j].is_obstacle = True

    def get_tile(self, x, y):
        return self.__body[x][y]
