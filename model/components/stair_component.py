from model.components.interfaces import Interactive
from model.components.interfaces import Visible
import model.dungeon as dungeon
from view.canvas_tile import CanvasTile
import tcod

class StairComponent(Interactive, Visible):

    def __init__(self, is_up):
        self.is_up = is_up  #boolean, whether up-stair or down-stair
        display_char = '<' if is_up else '>'
        self.canvas_tile = CanvasTile(None, tcod.Color(255,0,0), display_char)

    def set_destination_floor(self, floor):
        self.dest_floor = floor

    def interact(self, actor):
        if actor == dungeon.player:
            if self.is_up:
                dungeon.go_up_to_floor(self.dest_floor)
            else:
                dungeon.go_down_to_floor(self.dest_floor)

    def get_canvas_tile(self):
        return self.canvas_tile
