import tcod
import core

class PanelCanvas:

    default_canvas_tile = {
        "bgcolor": tcod.Color(0, 0, 0),
        "fgcolor": tcod.Color(100, 100, 100),
        "char": '#'
    }

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
        tcod.console_put_char_ex(core.root_console, self.x_offset + tile_x, self.y_offset + tile_y, ord(tile["char"]), tile["fgcolor"], tile["bgcolor"])

    def put_char(self, tile_x, tile_y, bgcolor, fgcolor, char):
        self.body[tile_y][tile_x] = {"bgcolor": bgcolor, "fgcolor": fgcolor, "char": char}
