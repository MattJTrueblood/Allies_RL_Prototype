from view.canvas_tile import CanvasTile
from model.dungeon_tile import DungeonTile
from model.stair_tile import StairTile
import model.dungeon as dungeon
import random
import tcod

class StubFloor:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__body = [[DungeonTile(CanvasTile(tcod.Color(0, 0, 0), tcod.Color(255, 255, 255), '.'), False) for i in range(height)] for j in range(width)]
        #make walls
        for i in range(width):
            for j in range(height):
                if i == 0 or j == 0 or i == width-1 or j == height-1:
                    self.__body[i][j].canvas_tile.character = '#'
                    self.__body[i][j].is_obstacle = True

        #make stairs
        self.upstair_x = random.randint(1, width-2)
        self.upstair_y = random.randint(1, height-2)
        while True:
            self.downstair_x = random.randint(1, width-2)
            self.downstair_y = random.randint(1, height-2)
            if self.downstair_x != self.upstair_x or self.downstair_y != self.upstair_y:
                break
        self.__body[self.upstair_x][self.upstair_y] = StairTile("up")
        self.__body[self.downstair_x][self.downstair_y] = StairTile("down")

    def get_tile(self, x, y):
        return self.__body[x][y]
