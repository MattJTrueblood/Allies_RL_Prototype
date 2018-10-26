from model.components.interfaces import Interactive
from model.components.base_component import BaseComponent
import model.dungeon as dungeon
from view.canvas_tile import CanvasTile
import tcod

class StairComponent(BaseComponent, Interactive):

    def __init__(self, parent_entity, is_up):
        super().__init__(parent_entity)
        self.is_up = is_up  #boolean, whether up-stair or down-stair

    def set_destination_floor(self, floor):
        self.dest_floor = floor

    def interact(self, actor):
        if actor == dungeon.player:
            if self.is_up:
                dungeon.go_up_to_floor(self.dest_floor)
            else:
                dungeon.go_down_to_floor(self.dest_floor)
