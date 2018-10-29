import tcod
import core
from view.canvas_tile import CanvasTile

class PanelCanvas:

    default_canvas_tile = CanvasTile(tcod.Color(0, 0, 0), tcod.Color(100, 100, 100), ' ')

    def __init__(self, x, y, width, height):
        self.x_offset = x
        self.y_offset = y
        self.width = width
        self.height = height
        self.body = [[None for i in range(self.width)] for j in range(self.height)]

    def render(self):
        for i in range(self.width):
            for j in range(self.height):
                tile = self.body[j][i]
                if not tile:
                    tile = PanelCanvas.default_canvas_tile
                self.__draw_tile(i, j, tile)

    def __draw_tile(self, tile_x, tile_y, tile):
        tcod.console_put_char_ex(core.root_console, self.x_offset + tile_x, self.y_offset + tile_y, ord(tile.character), tile.fgcolor, tile.bgcolor)

    def put_tile(self, tile_x, tile_y, tile):
        self.body[tile_y][tile_x] = tile

    def put_char(self, tile_x, tile_y, bgcolor, fgcolor, char):
        self.body[tile_y][tile_x] = CanvasTile(bgcolor, fgcolor, char)

    def get_tile(self, x, y):
        return self.body[y][x]

    def put_string(self, tile_x, tile_y, print_string, text_color, bgcolor=default_canvas_tile.bgcolor):
        if len(print_string) <= self.width - tile_x:
            for i, character in enumerate(print_string):
                self.put_char(tile_x + i, tile_y, bgcolor, text_color, character)
