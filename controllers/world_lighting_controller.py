import model.game as game
from view.panel_canvas import PanelCanvas
from view.canvas_tile import CanvasTile
from model.components.visible_component import VisibleComponent
from model.floor import Visibility
from model.utils.point import Point
import tcod

LOS_ROTATE_MATRIX = [
  [1,  0,  0, -1, -1,  0,  0,  1],
  [0,  1, -1,  0,  0, -1,  1,  0],
  [0,  1,  1,  0,  0, -1, -1,  0],
  [1,  0,  0,  1, -1,  0,  0, -1],
] # this is used by the lighting algorithm.  The lighting algorithm only works for 0-45 degrees
  # (clockwise) around the player.  This matrix can copy the logic so it works for all 360 degrees.

class WorldLightingController:

    def __init__(self, canvas):
        self.canvas = canvas
        self.visibility_map = 0

    def draw_canvas_with_lighting(self, panel_center_x, panel_center_y):

        #calculate which tiles are visible, seen, and unknown.
        self.visibility_map = game.current_floor.get_visibility_map()
        self.update_visibility_map()
        game.current_floor.set_visibility_map(self.visibility_map)

        #Draw current floor in viewport
        for i in range(self.canvas.width):
            for j in range(self.canvas.height):
                tile_to_draw = PanelCanvas.default_canvas_tile
                ij_world = self.canvas_coord_to_world_coord(panel_center_x, panel_center_y, i, j)
                if(self.world_coord_in_bounds(ij_world[0], ij_world[1])):
                    ij_visibility = self.get_world_coord_visibility(ij_world[0], ij_world[1])
                    if(ij_visibility == Visibility.VISIBLE):
                        tile_to_draw = game.current_floor.get_tile(ij_world[0], ij_world[1]).canvas_tile
                        game.current_floor.set_last_seen_tile(ij_world[0], ij_world[1], tile_to_draw)
                    elif(ij_visibility == Visibility.SEEN):
                        tile_to_draw = self.convert_tile_to_grayscale(game.current_floor.get_last_seen_tile(ij_world[0], ij_world[1]))
                self.canvas.put_tile(i, j, tile_to_draw)

        #Draw entities in viewport
        for entity in game.current_floor.get_entities():
            visible_component= entity.get_component(VisibleComponent)
            if visible_component:
                entity_xy_canvas = self.world_coord_to_canvas_coord(panel_center_x, panel_center_y, entity.x, entity.y)
                entity_xy_visible = self.get_world_coord_visibility(entity.x, entity.y)
                if(self.canvas_coord_in_bounds(entity_xy_canvas[0], entity_xy_canvas[1]) and entity_xy_visible == Visibility.VISIBLE):
                    entity_tile = visible_component.get_canvas_tile()
                    tile_to_draw = CanvasTile(self.canvas.get_tile(entity_xy_canvas[0], entity_xy_canvas[1]).bgcolor,
                            entity_tile.fgcolor, entity_tile.character)
                    self.canvas.put_tile(entity_xy_canvas[0], entity_xy_canvas[1], tile_to_draw)
                    game.current_floor.set_last_seen_tile(entity.x, entity.y, tile_to_draw)


    def update_visibility_map(self):
        for i in range(game.current_floor.width):
            for j in range(game.current_floor.height):
                visible_tile = self.visibility_map[i][j]
                if visible_tile == Visibility.VISIBLE:
                    # this will be overwritten by VISIBLE if still visible later in this function
                    self.visibility_map[i][j] = Visibility.SEEN

        visible_points = set()
        visible_points.add(Point(game.player.x, game.player.y))
        for region in range(8): # 8 quadrants, each 45 degrees
            self.cast_light(visible_points, game.player.x, game.player.y, 1, 1.0, 0.0, 30,
                LOS_ROTATE_MATRIX[0][region], LOS_ROTATE_MATRIX[1][region],
                LOS_ROTATE_MATRIX[2][region], LOS_ROTATE_MATRIX[3][region])
        for point in visible_points:
            self.visibility_map[point.x][point.y] = Visibility.VISIBLE

    def cast_light(self, visible_points, cx, cy, row, start, end, radius, xx, xy, yx, yy):
        if start < end:
            return

        radius_squared = radius * radius

        for j in range(row, radius + 1):
            dx, dy = -j-1, -j
            blocked = False
            while dx <= 0:
                dx += 1
                #translate dx, dy into map coords
                X, Y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
                point = Point(X, Y)
                #l_slope and r_slope store the slopes of the left and right extremities of the square we're considering:
                l_slope, r_slope = (dx - 0.5)/(dy+0.5), (dx+0.5)/(dy-0.5)
                if start < r_slope:
                    continue
                elif end > l_slope:
                    break
                else:
                    #Our light beam is touching this square; light it:
                    if dx*dx + dy*dy < radius_squared:
                        visible_points.add(point)
                    if blocked:
                        #scanning a row of blocked squares
                        if not self.get_allows_light(point):
                            new_start = r_slope
                            continue
                        else:
                            blocked = False
                            start = new_start
                    else:
                        if not self.get_allows_light(point) and j < radius:
                            #this is a blocking square, start a child scan
                            blocked = True
                            self.cast_light(visible_points, cx, cy, j+1, start, l_slope, radius, xx, xy, yx, yy)
                            new_start = r_slope
            #Row is scanned; do next row unless last square is blocked:
            if blocked:
                break


    def get_world_coord_visibility(self, x, y):
        return self.visibility_map[x][y]

    def get_allows_light(self, point):
        for entity in game.current_floor.get_entities():
            if(entity.x == point.x and entity.y == point.y):
                visible_component= entity.get_component(VisibleComponent)
                if visible_component:
                    if visible_component.get_obstructs_vision():
                        return False
        return game.current_floor.get_tile(point.x, point.y).is_transparent

    def convert_tile_to_grayscale(self, tile):
        newBgColor = int((tile.bgcolor.r + tile.bgcolor.g + tile.bgcolor.b) / 3.0)
        newFgColor = int((tile.fgcolor.r + tile.fgcolor.g + tile.fgcolor.b) / 3.0)
        tile.bgColor = tcod.Color(newBgColor, newBgColor, newBgColor)
        tile.fgColor = tcod.Color(newFgColor, newFgColor, newFgColor)
        return tile

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
