from model.components.base_component import BaseComponent

class VisibleComponent(BaseComponent):

    def __init__(self, parent_entity, canvas_tile):
        super().__init__(parent_entity)
        self.canvas_tile = canvas_tile

    def get_canvas_tile(self):
        return self.canvas_tile

    def set_canvas_tile(self, new_tile):
        self.canvas_tile = new_tile
