import model.game as game
from view.panel_canvas import PanelCanvas
from model.components.visible_component import VisibleComponent
from model.floor import Visibility

class WorldLightingController:

    def __init__(self, canvas):
        self.canvas = canvas

    def draw_canvas_with_lighting(self, panel_center_x, panel_center_y):

        #calculate which tiles are visible, seen, and unknown.
        visibility_map = game.current_floor.get_visibility_map()

        #Draw current floor in viewport
        for i in range(self.canvas.width):
            for j in range(self.canvas.height):
                ij_world = self.canvas_coord_to_world_coord(panel_center_x, panel_center_y, i, j)
                if(self.world_coord_in_bounds(ij_world[0], ij_world[1])):
                    tile_to_draw = game.current_floor.get_tile(ij_world[0], ij_world[1]).canvas_tile
                    self.canvas.put_tile(i, j, tile_to_draw)
                else:
                    self.canvas.put_tile(i, j, PanelCanvas.default_canvas_tile)

        #Draw entities in viewport
        for entity in game.current_floor.get_entities():
            visible_component= entity.get_component(VisibleComponent)
            if visible_component:
                entity_xy_canvas = self.world_coord_to_canvas_coord(panel_center_x, panel_center_y, entity.x, entity.y)
                if self.canvas_coord_in_bounds(entity_xy_canvas[0], entity_xy_canvas[1]):
                    tile_to_draw = visible_component.get_canvas_tile()
                    self.canvas.put_char(entity_xy_canvas[0], entity_xy_canvas[1],
                        self.canvas.get_tile(entity_xy_canvas[0], entity_xy_canvas[1]).bgcolor,
                        tile_to_draw.fgcolor, tile_to_draw.character)


    def canvas_coord_to_world_coord(self, panel_center_x, panel_center_y, x_canvas, y_canvas):
        x_world = game.player.x - panel_center_x + x_canvas
        y_world = game.player.y - panel_center_y + y_canvas
        return (x_world, y_world)

    def world_coord_to_canvas_coord(self, panel_center_x, panel_center_y, x_world, y_world):
        x_canvas = x_world + panel_center_x - game.player.x
        y_canvas = y_world + panel_center_y - game.player.y
        return (x_canvas, y_canvas)

    def world_coord_in_bounds(self, world_x, world_y):
        return world_x >= 0 and world_x < game.current_floor.width and world_y >= 0 and world_y < game.current_floor.height

    def canvas_coord_in_bounds(self, canvas_x, canvas_y):
        return canvas_x >= 0 and canvas_x < self.canvas.width and canvas_y >= 0 and canvas_y < self.canvas.height
