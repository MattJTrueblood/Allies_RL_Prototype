import model.game as game
from view.canvas_tile import CanvasTile
from model.dungeon_tile import DungeonTile
import tcod

class StairTile(DungeonTile):

    def __init__(self, dir):
        if(dir == "up"):
            super().__init__(CanvasTile(tcod.Color(0, 0, 0), tcod.Color(255, 0, 0), '<'), False)
        elif(dir == "down"):
            super().__init__(CanvasTile(tcod.Color(0, 0, 0), tcod.Color(255, 0, 0), '>'), False)
        self.dir = dir

    def on_interact(self):
        if(self.dir == "up"):
            game.go_to_prev_floor()
        if(self.dir == "down"):
            game.go_to_next_floor()
