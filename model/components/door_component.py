from model.components.base_component import BaseComponent
from model.components.interfaces import MoveInteractive, AdjacentInteractive
from model.components.tags import CanOpenDoors, ObstructsMovement
from model.components.visible_component import VisibleComponent
from view.canvas_tile import CanvasTile
import tcod

class DoorComponent(BaseComponent, MoveInteractive, AdjacentInteractive):

    OPEN_TILE = CanvasTile(None, tcod.Color(205, 133, 63), '-')
    CLOSED_TILE = CanvasTile(None, tcod.Color(205, 133, 63), '+')

    def __init__(self, parent_entity, closed=True):
        super().__init__(parent_entity)
        self.closed = closed

    def interact_adjacent(self, actor):
        if actor.get_component(CanOpenDoors):
            self.toggle_open_closed()

    def interact_move(self, actor):
        if actor.get_component(CanOpenDoors) and self.closed:  #should only work if it's closed
            self.toggle_open_closed()

    def toggle_open_closed(self):
        self.closed = False if self.closed else True
        self.update_visible_component()

    def update_visible_component(self):
        visible_component = self.parent_entity.get_component(VisibleComponent)
        if(self.closed):
            visible_component.set_canvas_tile(DoorComponent.CLOSED_TILE)
            self.parent_entity.get_component_including_disabled(ObstructsMovement).enable()
        else:
            visible_component.set_canvas_tile(DoorComponent.OPEN_TILE)
            self.parent_entity.get_component(ObstructsMovement).disable()
