from model.components.interfaces import GroundInteractive
from model.components.base_component import BaseComponent
import model.game as game
from view.canvas_tile import CanvasTile
import tcod

class StairComponent(BaseComponent, GroundInteractive):

    def __init__(self, parent_entity, is_up):
        super().__init__(parent_entity)
        self.is_up = is_up  #boolean, whether up-stair or down-stair

    def set_destination_floor(self, floor):
        self.dest_floor = floor

    def interact_ground(self, actor):
        if actor == game.player:
            if self.is_up:
                game.go_up_to_floor(self.dest_floor)
            else:
                game.go_down_to_floor(self.dest_floor)
