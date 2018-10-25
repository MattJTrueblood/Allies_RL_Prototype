from model.tile import Tile
import tcod

class StubFloor:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.body = [[Tile(tcod.Color(0, 0, 0), tcod.Color(255, 255, 255), '.') for i in range(width)] for j in range(height)]
        #draw border
        for i in range(width):
            for j in range(height):
                if i == 0 or j == 0 or i == width-1 or j == height-1:
                    self.body[i][j] = Tile(tcod.Color(100, 100, 100), tcod.Color(255, 255, 255), '#')
